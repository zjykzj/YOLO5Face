# -*- coding: utf-8 -*-

"""
@Time    : 2024/7/14 10:17
@File    : model.py
@Author  : zj
@Description: 
"""

import torch

from models.yolo5face.comonents import StemBlock, ShuffleV2Block


def test_stemblock():
    model = StemBlock(3, 64, k=3, s=2)
    model.eval()
    data = torch.randn(2, 3, 640, 640)

    res = model(data)
    print(f"data shape: {data.shape} - res shape: {res.shape}")


def test_shufflev2block():
    model = ShuffleV2Block(3, 128, 2)
    model.eval()
    data = torch.randn(2, 3, 640, 640)

    res = model(data)
    print(f"data shape: {data.shape} - res shape: {res.shape}")

    model = ShuffleV2Block(256, 256, 1)
    model.eval()
    data = torch.randn(2, 128, 640, 640)

    res = model(data)
    print(f"data shape: {data.shape} - res shape: {res.shape}")


if __name__ == '__main__':
    # test_stemblock()
    test_shufflev2block()
