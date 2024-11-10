# -*- coding: utf-8 -*-

"""
@date: 2024/11/10 下午3:15
@file: draw_wing_loss_v2.py
@author: zj
@Description: 绘制Wing Loss和L2 Loss
"""

import numpy as np
import matplotlib.pyplot as plt


def calculate_wing_loss(y_hat, y_true, w, e):
    """
    计算Wing Loss
    :param y_hat: 预测值数组
    :param y_true: 真实值
    :param w: Wing Loss的w参数
    :param e: Wing Loss的e参数
    :return: Wing Loss数组
    """
    C = w - w * np.log(1 + w / e)
    abs_diff = np.abs(y_hat - y_true)
    loss = np.where(abs_diff < w,
                    w * np.log(1 + abs_diff / e),
                    abs_diff - C)
    return loss


def calculate_l2_loss(y_hat, y_true):
    """
    计算L2 Loss
    :param y_hat: 预测值数组
    :param y_true: 真实值
    :return: L2 Loss数组
    """
    return 0.5 * (y_hat - y_true) ** 2


def plot_losses(y_hat, y_true, w, e):
    """
    绘制Wing Loss和L2 Loss
    :param y_hat: 预测值数组
    :param y_true: 真实值
    :param w: Wing Loss的w参数
    :param e: Wing Loss的e参数
    """
    wing_loss_values = calculate_wing_loss(y_hat, y_true, w, e)
    l2_loss_values = calculate_l2_loss(y_hat, y_true)

    plt.figure(figsize=(10, 6))

    plt.plot(y_hat, wing_loss_values, label='Wing Loss', color='blue')
    plt.plot(y_hat, l2_loss_values, label='L2 Loss', color='green')

    plt.scatter([y_true], [0], color='red', zorder=3)  # 真实值点

    plt.title('Comparison of Wing Loss and L2 Loss')
    plt.xlabel('Prediction ($\hat{y}$)')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    # 定义超参数
    w = 10
    e = 2

    # 定义预测值范围
    y_hat = np.linspace(-20, 20, 200)
    # 真实值设为0
    y_true = 0

    # 绘制损失函数图形
    plot_losses(y_hat, y_true, w, e)
