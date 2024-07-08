# -*- coding: utf-8 -*-

"""
@date: 2024/6/23 下午8:14
@file: model.py
@author: zj
@description:

"""

import cv2
import numpy as np
import torch

from models.yolo5face.general import non_max_suppression, scale_landmarks
from utils.general import TQDM_BAR_FORMAT, colorstr, scale_boxes


def test_nms():
    pred = np.load("../assets/widerface/0_Parade_marchingband_1_1004/nms_before.npy")
    pred = np.concatenate((pred[..., :5], pred[..., -1:], pred[..., 5:-1]), axis=-1)
    print(f"pred shape: {pred.shape}")

    img1_shape = (512, 640)
    conf_thres = 0.25
    iou_thres = 0.45
    pred = non_max_suppression(torch.from_numpy(pred),
                               conf_thres,
                               iou_thres,
                               labels=(),
                               multi_label=False,
                               agnostic=False,
                               max_det=300)
    print(len(pred[0]), 'face' if len(pred[0]) == 1 else 'faces')

    img_path = "../assets/widerface/0_Parade_marchingband_1_1004.jpg"
    img = cv2.imread(img_path)
    print(f"img type: {type(img)} - dtype: {img.dtype} - shape: {img.shape}")

    det = pred[0]
    det[:, :4] = scale_boxes(img1_shape, det[:, :4], img.shape[:2]).round()
    det[:, 6:] = scale_landmarks(img1_shape, det[:, 6:], img.shape[:2]).round()
    for item in det:
        print(item)
        x_min, y_min, x_max, y_max = item[:4]
        cv2.rectangle(img, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 1)

        for kp in item[6:].reshape(-1, 2):
            x, y = kp
            if x < 0 or y < 0:
                continue
            cv2.circle(img, (int(x), int(y)), 1, (0, 0, 255), -1)

    cv2.imshow("img", img)
    cv2.waitKey(0)


if __name__ == '__main__':
    test_nms()
