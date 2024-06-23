# -*- coding: utf-8 -*-

"""
@date: 2024/6/23 下午8:14
@file: model.py
@author: zj
@description: 
"""

import torch

from models.yolo import Model
from models.common import Conv
from models.yolo5face.comonents import StemBlock


def test1():
    model1 = Conv(3, 64, 6, 2, 2)
    model2 = StemBlock(3, 64, 3, 2, )

    data = torch.randn(1, 3, 640, 640)
    res1 = model1(data)
    res2 = model2(data)
    print(res1.shape, res2.shape)


if __name__ == '__main__':
    cfg1 = "models/yolo5face/cfgs/yolov5s_face.yaml"
    model1 = Model(cfg1, ch=3, nc=80, anchors=None)  # create
    model1.train()
    print(model1)

    cfg2 = "models/yolov5s.yaml"
    model2 = Model(cfg2, ch=3, nc=80, anchors=None)  # create
    model2.train()
    print(model2)

    data = torch.randn(1, 3, 640, 640)
    res1 = model1(data)
    res2 = model2(data)
    for item1, item2 in zip(res1, res2):
        print(item1.shape, item2.shape)
