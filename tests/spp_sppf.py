# -*- coding: utf-8 -*-

"""
@date: 2024/11/9 下午10:48
@file: spp_sppf.py
@author: zj
@description: 
"""

import torch

# Profile
from utils.torch_utils import profile
from models.common import SPP, SPPF

m1 = SPP(512, 512, k=(5, 9, 13))
m2 = SPPF(512, 512, k=5)
results = profile(input=torch.randn(1, 512, 32, 32), ops=[m1, m2], n=10)
results = profile(input=torch.randn(1, 512, 16, 16), ops=[m1, m2], n=10)

m1 = SPP(512, 1024, k=(3, 5, 7))
m2 = SPPF(512, 1024, k=3)
results = profile(input=torch.randn(1, 512, 32, 32), ops=[m1, m2], n=10)
results = profile(input=torch.randn(1, 512, 16, 16), ops=[m1, m2], n=10)
