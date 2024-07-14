# -*- coding: utf-8 -*-

"""
@date: 2024/6/21 下午8:14
@file: model.py
@author: zj
@description:

"""

import cv2
import numpy as np
import torch

from models.yolo5face.general import non_max_suppression, scale_landmarks
from utils.general import scale_boxes


def process(pred_path, img_path, im_shape):
    # pred = np.load("../assets/widerface/0_Parade_marchingband_1_1004/nms_before.npy")
    pred = np.load(pred_path)
    print(f"pred shape: {pred.shape}")

    # img_path = "../assets/widerface/0_Parade_marchingband_1_1004.jpg"
    img = cv2.imread(img_path)
    print(f"img type: {type(img)} - dtype: {img.dtype} - shape: {img.shape}")

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

    det = pred[0]
    det[:, :4] = scale_boxes(im_shape, det[:, :4], img.shape[:2]).round()
    det[:, 6:] = scale_landmarks(im_shape, det[:, 6:], img.shape[:2]).round()
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


def test_nms():
    pred_path_list = [
        "./pred/0_Parade_marchingband_1_1004.npy",
        "./pred/10_People_Marching_People_Marching_2_773.npy",
    ]
    img_path_list = [
        "../assets/widerface/0_Parade_marchingband_1_1004.jpg",
        "../assets/widerface/10_People_Marching_People_Marching_2_773.jpg",
    ]
    im_shape_list = [
        [480, 640],
        [480, 640],
    ]
    for pred_path, img_path, im_shape in zip(pred_path_list, img_path_list, im_shape_list):
        process(pred_path, img_path, im_shape)


if __name__ == '__main__':
    test_nms()
