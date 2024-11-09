# -*- coding: utf-8 -*-

"""
@Time    : 2024/7/14 10:17
@File    : model.py
@Author  : zj
@Description: 
"""

import torch

from utils.torch_utils import profile
from models.yolo5face.comonents import StemBlock, ShuffleV2Block


def test_stemblock():
    model = StemBlock(3, 64, k=3, s=2)
    model.eval()
    data = torch.randn(2, 3, 640, 640)

    res = model(data)
    print(f"data shape: {data.shape} - res shape: {res.shape}")

    profile(data, model)


def test_shufflev2block():
    m1 = ShuffleV2Block(3, 128, 2)
    m1.eval()
    data = torch.randn(2, 3, 640, 640)

    res = m1(data)
    print(f"data shape: {data.shape} - res shape: {res.shape}")

    m2 = ShuffleV2Block(256, 256, 1)
    m2.eval()
    data = torch.randn(2, 256, 640, 640)

    res = m2(data)
    print(f"data shape: {data.shape} - res shape: {res.shape}")

    profile(data, [m1, m2])


if __name__ == '__main__':
    print(f"*" * 100)
    test_stemblock()
    print(f"*" * 100)
    test_shufflev2block()
