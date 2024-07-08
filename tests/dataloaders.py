# -*- coding: utf-8 -*-

"""
@date: 2024/7/7 下午7:54
@file: dataloaders.py
@author: zj
@description: 
"""

import cv2
import yaml

from tqdm import tqdm
import numpy as np

from models.yolo5face.dataloaders import LoadImagesAndLabels, create_dataloader
from utils.general import TQDM_BAR_FORMAT, colorstr


def show_image_by_dataset(dataset):
    for index in np.random.choice(len(dataset), size=5, replace=False):
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


def show_image_by_dataloader(dataloader):
    total = 5

    nb = len(dataloader)  # number of batches
    pbar = enumerate(dataloader)
    pbar = tqdm(pbar, total=total, bar_format=TQDM_BAR_FORMAT)  # progress bar
    for i, (imgs, targets, paths, _) in pbar:  # batch -------------------------------------------------------------
        for idx, img in enumerate(imgs):
            labels = targets[targets[:, 0] == idx]

            # CHW to HWC, RGB to BGR
            img = img.numpy().transpose((1, 2, 0))[..., ::-1]
            img = np.ascontiguousarray(img)

            img_h, img_w = img.shape[:2]
            # print(f"img type: {type(img)} - dtype: {img.dtype} - shape: {img.shape}")

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
        if (i + 1) >= total:
            break


def create_dataset(is_train=False):
    hyp = "../models/yolo5face/hyps/hyp.scratch-low.yaml"
    with open(hyp, errors='ignore') as f:
        hyp = yaml.safe_load(f)  # load hyps dict

    # path = '/home/zj/datasets/widerface/images/train'
    path = r'C:\zj\repos\datasets\widerface\images\train'
    dataset = LoadImagesAndLabels(path, img_size=640, batch_size=1, augment=is_train, hyp=hyp)

    return dataset


def test_dataset():
    print('*' * 100 + " Eval")
    dataset = create_dataset(is_train=False)
    print(dataset)
    show_image_by_dataset(dataset)

    print('*' * 100 + " Train")
    dataset = create_dataset(is_train=True)
    print(dataset)
    show_image_by_dataset(dataset)


def test_dataloader():
    hyp = "../models/yolo5face/hyps/hyp.scratch-low.yaml"
    with open(hyp, errors='ignore') as f:
        hyp = yaml.safe_load(f)  # load hyps dict

    imgsz = 640
    batch_size = 1
    stride = 32

    print('*' * 100 + " Eval")
    # valloader
    val_path = r'C:\zj\repos\datasets\widerface\images\train'
    val_loader = create_dataloader(val_path,
                                   imgsz,
                                   batch_size,
                                   stride,
                                   single_cls=False,
                                   hyp=hyp,
                                   rect=True,
                                   rank=-1,
                                   workers=2,
                                   pad=0.5,
                                   prefix=colorstr('val: '))[0]
    show_image_by_dataloader(val_loader)

    print('*' * 100 + " Train")
    # Trainloader
    train_path = r'C:\zj\repos\datasets\widerface\images\train'
    train_loader, dataset = create_dataloader(train_path,
                                              imgsz,
                                              batch_size,
                                              stride,
                                              single_cls=False,
                                              hyp=hyp,
                                              augment=True,
                                              prefix=colorstr('train: '),
                                              shuffle=True)
    show_image_by_dataloader(train_loader)


if __name__ == '__main__':
    test_dataset()
    test_dataloader()
