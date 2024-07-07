# -*- coding: utf-8 -*-

"""
@date: 2024/7/7 下午7:54
@file: dataloaders.py
@author: zj
@description: 
"""

import cv2
import yaml

import numpy as np

from models.yolo5face.dataloaders import LoadImagesAndLabels


def show_image(dataset):
    for index in np.random.choice(len(dataset), size=10, replace=False):
        img, labels, img_path, shapes = dataset.__getitem__(index)

        # CHW to HWC, RGB to BGR
        img = img.numpy().transpose((1, 2, 0))[..., ::-1]
        img = np.ascontiguousarray(img)

        img_h, img_w = img.shape[:2]
        print(f"img type: {type(img)} - dtype: {img.dtype} - shape: {img.shape}")

        for item in labels.numpy():
            x_c, y_c, box_w, box_h = item[2:6]
            x_min = (x_c - box_w / 2) * img_w
            y_min = (y_c - box_h / 2) * img_h
            x_max = (x_c + box_w / 2) * img_w
            y_max = (y_c + box_h / 2) * img_h

            cv2.rectangle(img, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 1)

            for kp in item[6:].reshape(-1, 2):
                x, y = kp
                if x < 0 or y < 0:
                    continue
                x = int(x * img_w)
                y = int(y * img_h)

                cv2.circle(img, (x, y), 1, (0, 0, 255), -1)

        cv2.imshow("img", img)
        cv2.waitKey(0)


def create_dataset(is_train=False):
    hyp = "../models/yolo5face/hyps/hyp.scratch-low.yaml"
    with open(hyp, errors='ignore') as f:
        hyp = yaml.safe_load(f)  # load hyps dict

    path = '/home/zj/datasets/widerface/images/train'
    dataset = LoadImagesAndLabels(path, img_size=640, batch_size=1, augment=is_train, hyp=hyp)

    return dataset


def test_dataset():
    print('*' * 100 + " Eval")
    dataset = create_dataset(is_train=False)
    print(dataset)
    show_image(dataset)

    print('*' * 100 + " Train")
    dataset = create_dataset(is_train=True)
    print(dataset)
    show_image(dataset)


if __name__ == '__main__':
    # create_dataset()
    test_dataset()
