# -*- coding: utf-8 -*-

"""
@date: 2024/6/23 下午8:12
@file: comonents.py
@author: zj
@description: 
"""

import numpy as np

import torch
import torch.nn as nn

from models.common import Conv
from utils.general import check_version


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
