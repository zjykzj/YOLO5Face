# -*- coding: utf-8 -*-

"""
@date: 2024/11/10 下午3:04
@file: draw_landmarks_v2.py
@author: zj
@description: 绘制人脸框及关键点
"""

import os
import cv2
import numpy as np


def draw_keypoints(image, landmarks, img_w, img_h):
    """
    在图像上绘制关键点
    :param image: 输入图像
    :param landmarks: 关键点列表，每个关键点是一个包含两个元素（x, y）的列表
    :param img_w: 图像宽度
    :param img_h: 图像高度
    """
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255)]  # 不同的颜色用于不同关键点
    shapes = [cv2.MARKER_CROSS, cv2.MARKER_TILTED_CROSS, cv2.MARKER_STAR, cv2.MARKER_DIAMOND, cv2.MARKER_SQUARE]

    for i, (x, y) in enumerate(landmarks):
        x = int(x * img_w)
        y = int(y * img_h)
        cv2.drawMarker(image, (x, y), colors[i], markerType=shapes[i], markerSize=10, thickness=2)


def main():
    # img_path = "./assets/widerface_train/28_Sports_Fan_Sports_Fan_28_56.jpg"
    img_path = "./assets/widerface_train/28_Sports_Fan_Sports_Fan_28_650.jpg"
    img = cv2.imread(img_path)
    img_h, img_w = img.shape[:2]

    # txt_path = "./assets/widerface_train/28_Sports_Fan_Sports_Fan_28_56.txt"
    txt_path = "./assets/widerface_train/28_Sports_Fan_Sports_Fan_28_650.txt"
    label_array = np.loadtxt(txt_path, dtype=float, delimiter=' ')

    for item in label_array:
        cls_id = item[0]
        truth_box = item[1:5]
        landmarks = item[5:].reshape(-1, 2)

        if -1 not in landmarks:
            truth_box[::2] *= img_w
            truth_box[1::2] *= img_h
            x_c, y_c, box_w, box_h = truth_box.astype(int)
            x_min = int(x_c - box_w / 2)
            y_min = int(y_c - box_h / 2)
            x_max = int(x_c + box_w / 2)
            y_max = int(y_c + box_h / 2)
            cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 0, 255), 1)

            # 调用绘制关键点函数
            draw_keypoints(img, landmarks, img_w, img_h)

    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imwrite("./assets/draw_landmarks.jpg", img)


if __name__ == '__main__':
    main()
