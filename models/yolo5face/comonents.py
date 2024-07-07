# -*- coding: utf-8 -*-

"""
@date: 2024/6/23 下午8:12
@file: comonents.py
@author: zj
@description: 
"""

import time
import numpy as np

import torch
import torch.nn as nn
import torchvision

from models.common import Conv
from utils.general import check_version, LOGGER, xywh2xyxy
from utils.metrics import box_iou


class StemBlock(nn.Module):

    def __init__(self, c1, c2, k=3, s=2, p=None, g=1, act=True):
        super(StemBlock, self).__init__()
        self.stem_1 = Conv(c1, c2, k=k, s=s, p=p, g=g, act=act)
        self.stem_2a = Conv(c2, c2 // 2, 1, 1, 0)
        self.stem_2b = Conv(c2 // 2, c2, 3, 2, 1)
        self.stem_2p = nn.MaxPool2d(kernel_size=2, stride=2, ceil_mode=True)
        self.stem_3 = Conv(c2 * 2, c2, 1, 1, 0)

    def forward(self, x):
        stem_1_out = self.stem_1(x)
        stem_2a_out = self.stem_2a(stem_1_out)
        stem_2b_out = self.stem_2b(stem_2a_out)
        stem_2p_out = self.stem_2p(stem_1_out)
        out = self.stem_3(torch.cat((stem_2b_out, stem_2p_out), 1))
        return out


class Detect(nn.Module):
    # YOLOv5 Detect head for detection models
    stride = None  # strides computed during build
    dynamic = False  # force grid reconstruction
    export = False  # export mode

    def __init__(self, nc=80, anchors=(), ch=(), inplace=True):  # detection layer
        super().__init__()
        self.nc = nc  # number of classes
        self.n_landmarks = 10  # number of landmarks
        # self.no = nc + 5   # number of outputs per anchor
        self.no = nc + 5 + self.n_landmarks  # number of outputs per anchor
        self.nl = len(anchors)  # number of detection layers
        self.na = len(anchors[0]) // 2  # number of anchors
        self.grid = [torch.empty(0) for _ in range(self.nl)]  # init grid
        self.anchor_grid = [torch.empty(0) for _ in range(self.nl)]  # init anchor grid
        self.register_buffer('anchors', torch.tensor(anchors).float().view(self.nl, -1, 2))  # shape(nl,na,2)
        self.m = nn.ModuleList(nn.Conv2d(x, self.no * self.na, 1) for x in ch)  # output conv
        self.inplace = inplace  # use inplace ops (e.g. slice assignment)

    def forward(self, x):
        z = []  # inference output
        for i in range(self.nl):
            x[i] = self.m[i](x[i])  # conv
            bs, _, ny, nx = x[i].shape  # x(bs,255,20,20) to x(bs,3,20,20,85)
            x[i] = x[i].view(bs, self.na, self.no, ny, nx).permute(0, 1, 3, 4, 2).contiguous()

            if not self.training:  # inference
                if self.dynamic or self.grid[i].shape[2:4] != x[i].shape[2:4]:
                    self.grid[i], self.anchor_grid[i] = self._make_grid(nx, ny, i)

                # Detect (boxes only)
                # xy, wh, conf = x[i].sigmoid().split((2, 2, self.nc + 1), 4)
                x[i] = torch.sigmoid(x[i][..., np.r_[0:5, (5 + self.n_landmarks):self.no]])
                xy, wh, conf, landmarks, cls = x[i].split((2, 2, 1, self.n_landmarks, self.nc), 4)
                xy = (xy * 2 + self.grid[i]) * self.stride[i]  # xy
                wh = (wh * 2) ** 2 * self.anchor_grid[i]  # wh

                landmarks = landmarks.reshape(bs, -1, 2)
                landmarks = landmarks * self.anchor_grid[i].reshape(bs, -1, 2) + self.grid[i] * self.stride[i]
                landmarks = landmarks.reshape(bs, -1)
                # landmarks[..., :2] = landmarks[..., :2] * self.anchor_grid[i] + self.grid[i] * self.stride[i]
                # landmarks[..., 2:4] = landmarks[..., 2:4] * self.anchor_grid[i] + self.grid[i] * self.stride[i]
                # landmarks[..., 4:6] = landmarks[..., 4:6] * self.anchor_grid[i] + self.grid[i] * self.stride[i]
                # landmarks[..., 6:8] = landmarks[..., 6:8] * self.anchor_grid[i] + self.grid[i] * self.stride[i]
                # landmarks[..., 8:10] = landmarks[..., 8:10] * self.anchor_grid[i] + self.grid[i] * self.stride[i]

                # y = torch.cat((xy, wh, conf), 4)
                y = torch.cat((xy, wh, conf, landmarks, cls), 4)
                z.append(y.view(bs, self.na * nx * ny, self.no))

        return x if self.training else (torch.cat(z, 1),) if self.export else (torch.cat(z, 1), x)

    def _make_grid(self, nx=20, ny=20, i=0, torch_1_10=check_version(torch.__version__, '1.10.0')):
        d = self.anchors[i].device
        t = self.anchors[i].dtype
        shape = 1, self.na, ny, nx, 2  # grid shape
        y, x = torch.arange(ny, device=d, dtype=t), torch.arange(nx, device=d, dtype=t)
        yv, xv = torch.meshgrid(y, x, indexing='ij') if torch_1_10 else torch.meshgrid(y, x)  # torch>=0.7 compatibility
        grid = torch.stack((xv, yv), 2).expand(shape) - 0.5  # add grid offset, i.e. y = 2.0 * x - 0.5
        anchor_grid = (self.anchors[i] * self.stride[i]).view((1, self.na, 1, 1, 2)).expand(shape)
        return grid, anchor_grid


def non_max_suppression(
        prediction,
        conf_thres=0.25,
        iou_thres=0.45,
        classes=None,
        agnostic=False,
        multi_label=False,
        labels=(),
        max_det=300,
        nm=0,  # number of masks
):
    """Non-Maximum Suppression (NMS) on inference results to reject overlapping detections

    Returns:
         # list of detections, on (n,6) tensor per image [xyxy, conf, cls]
         list of detections, on (n,16) tensor per image [xyxy, conf, cls, landmarks]
    """

    if isinstance(prediction, (list, tuple)):  # YOLOv5 model in validation model, output = (inference_out, loss_out)
        prediction = prediction[0]  # select only inference output

    device = prediction.device
    mps = 'mps' in device.type  # Apple MPS
    if mps:  # MPS not fully supported yet, convert tensors to CPU before NMS
        prediction = prediction.cpu()
    bs = prediction.shape[0]  # batch size
    # nc = prediction.shape[2] - nm - 5  # number of classes
    nc = prediction.shape[2] - nm - 10 - 5  # number of classes
    xc = prediction[..., 4] > conf_thres  # candidates

    # Checks
    assert 0 <= conf_thres <= 1, f'Invalid Confidence threshold {conf_thres}, valid values are between 0.0 and 1.0'
    assert 0 <= iou_thres <= 1, f'Invalid IoU {iou_thres}, valid values are between 0.0 and 1.0'

    # Settings
    # min_wh = 2  # (pixels) minimum box width and height
    max_wh = 7680  # (pixels) maximum box width and height
    max_nms = 30000  # maximum number of boxes into torchvision.ops.nms()
    time_limit = 0.5 + 0.05 * bs  # seconds to quit after
    redundant = True  # require redundant detections
    multi_label &= nc > 1  # multiple labels per box (adds 0.5ms/img)
    merge = False  # use merge-NMS

    t = time.time()
    # mi = 5 + nc  # mask start index
    # output = [torch.zeros((0, 6 + nm), device=prediction.device)] * bs
    li = 5 + nc
    mi = 5 + nc + 10  # mask start index
    output = [torch.zeros((0, 6 + 10 + nm), device=prediction.device)] * bs
    for xi, x in enumerate(prediction):  # image index, image inference
        # Apply constraints
        # x[((x[..., 2:4] < min_wh) | (x[..., 2:4] > max_wh)).any(1), 4] = 0  # width-height
        x = x[xc[xi]]  # confidence

        # # Cat apriori labels if autolabelling
        # if labels and len(labels[xi]):
        #     lb = labels[xi]
        #     v = torch.zeros((len(lb), nc + nm + 5), device=x.device)
        #     v[:, :4] = lb[:, 1:5]  # box
        #     v[:, 4] = 1.0  # conf
        #     v[range(len(lb)), lb[:, 0].long() + 5] = 1.0  # cls
        #     x = torch.cat((x, v), 0)

        # If none remain process next image
        if not x.shape[0]:
            continue

        # Compute conf
        # x[:, 5:] *= x[:, 4:5]  # conf = obj_conf * cls_conf
        x[:, 5:li] *= x[:, 4:5]  # conf = obj_conf * cls_conf

        # Box/Mask
        box = xywh2xyxy(x[:, :4])  # center_x, center_y, width, height) to (x1, y1, x2, y2)
        landmarks = x[:, li:mi]  # center_x, center_y, width, height) to (x1, y1, x2, y2)
        mask = x[:, mi:]  # zero columns if no masks

        # Detections matrix nx6 (xyxy, conf, cls)
        # if multi_label:
        #     i, j = (x[:, 5:mi] > conf_thres).nonzero(as_tuple=False).T
        #     x = torch.cat((box[i], x[i, 5 + j, None], j[:, None].float(), mask[i]), 1)
        # else:  # best class only
        #     conf, j = x[:, 5:mi].max(1, keepdim=True)
        #     x = torch.cat((box, conf, j.float(), mask), 1)[conf.view(-1) > conf_thres]
        # best class only
        # conf, j = x[:, 5:mi].max(1, keepdim=True)
        conf, j = x[:, 5:li].max(1, keepdim=True)
        x = torch.cat((box, conf, j.float(), landmarks, mask), 1)[conf.view(-1) > conf_thres]

        # # Filter by class
        if classes is not None:
            x = x[(x[:, 5:6] == torch.tensor(classes, device=x.device)).any(1)]

        # Apply finite constraint
        # if not torch.isfinite(x).all():
        #     x = x[torch.isfinite(x).all(1)]

        # Check shape
        n = x.shape[0]  # number of boxes
        if not n:  # no boxes
            continue
        elif n > max_nms:  # excess boxes
            x = x[x[:, 4].argsort(descending=True)[:max_nms]]  # sort by confidence
        else:
            x = x[x[:, 4].argsort(descending=True)]  # sort by confidence

        # Batched NMS
        c = x[:, 5:6] * (0 if agnostic else max_wh)  # classes
        boxes, scores = x[:, :4] + c, x[:, 4]  # boxes (offset by class), scores
        i = torchvision.ops.nms(boxes, scores, iou_thres)  # NMS
        if i.shape[0] > max_det:  # limit detections
            i = i[:max_det]
        if merge and (1 < n < 3E3):  # Merge NMS (boxes merged using weighted mean)
            # update boxes as boxes(i,4) = weights(i,n) * boxes(n,4)
            iou = box_iou(boxes[i], boxes) > iou_thres  # iou matrix
            weights = iou * scores[None]  # box weights
            x[i, :4] = torch.mm(weights, x[:, :4]).float() / weights.sum(1, keepdim=True)  # merged boxes
            if redundant:
                i = i[iou.sum(1) > 1]  # require redundancy

        output[xi] = x[i]
        if mps:
            output[xi] = output[xi].to(device)
        if (time.time() - t) > time_limit:
            LOGGER.warning(f'WARNING ⚠️ NMS time limit {time_limit:.3f}s exceeded')
            break  # time limit exceeded

    return output
