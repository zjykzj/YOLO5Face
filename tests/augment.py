# -*- coding: utf-8 -*-

"""
@Time    : 2024/11/4 16:23
@File    : custom_data.py
@Author  : zj
@Description: 
"""
import copy
import os.path

import cv2
import math
import random

import numpy as np

from utils.general import clip_boxes, xyxy2xywhn, xywhn2xyxy, xyn2xy
from utils.augmentations import box_candidates, letterbox


def load_image(f, img_size=640, augment=True):
    # Loads 1 image from dataset index 'i', returns (im, original hw, resized hw)
    im = cv2.imread(f)  # BGR
    assert im is not None, f'Image Not Found {f}'
    h0, w0 = im.shape[:2]  # orig hw
    r = img_size / max(h0, w0)  # ratio
    if r != 1:  # if sizes are not equal
        interp = cv2.INTER_LINEAR if (augment or r > 1) else cv2.INTER_AREA
        im = cv2.resize(im, (int(w0 * r), int(h0 * r)), interpolation=interp)
    return im, (h0, w0), im.shape[:2]  # im, hw_original, hw_resized


def random_perspective(im,
                       targets=(),
                       degrees=10,
                       translate=.1,
                       scale=.1,
                       shear=10,
                       perspective=0.0,
                       border=(0, 0)):
    # torchvision.transforms.RandomAffine(degrees=(-10, 10), translate=(0.1, 0.1), scale=(0.9, 1.1), shear=(-10, 10))
    # targets = [cls, xyxy]
    # use targets = [cls, xyxy, landmarks] instead

    height = im.shape[0] + border[0] * 2  # shape(h,w,c)
    width = im.shape[1] + border[1] * 2

    # Center
    C = np.eye(3)
    C[0, 2] = -im.shape[1] / 2  # x translation (pixels)
    C[1, 2] = -im.shape[0] / 2  # y translation (pixels)

    # Perspective
    P = np.eye(3)
    P[2, 0] = random.uniform(-perspective, perspective)  # x perspective (about y)
    P[2, 1] = random.uniform(-perspective, perspective)  # y perspective (about x)

    # Rotation and Scale
    R = np.eye(3)
    a = random.uniform(-degrees, degrees)
    # a += random.choice([-180, -90, 0, 90])  # add 90deg rotations to small rotations
    s = random.uniform(1 - scale, 1 + scale)
    # s = 2 ** random.uniform(-scale, scale)
    R[:2] = cv2.getRotationMatrix2D(angle=a, center=(0, 0), scale=s)

    # Shear
    S = np.eye(3)
    S[0, 1] = math.tan(random.uniform(-shear, shear) * math.pi / 180)  # x shear (deg)
    S[1, 0] = math.tan(random.uniform(-shear, shear) * math.pi / 180)  # y shear (deg)

    # Translation
    T = np.eye(3)
    T[0, 2] = random.uniform(0.5 - translate, 0.5 + translate) * width  # x translation (pixels)
    T[1, 2] = random.uniform(0.5 - translate, 0.5 + translate) * height  # y translation (pixels)

    # Combined rotation matrix
    M = T @ S @ R @ P @ C  # order of operations (right to left) is IMPORTANT
    if (border[0] != 0) or (border[1] != 0) or (M != np.eye(3)).any():  # image changed
        if perspective:
            im = cv2.warpPerspective(im, M, dsize=(width, height), borderValue=(114, 114, 114))
        else:  # affine
            im = cv2.warpAffine(im, M[:2], dsize=(width, height), borderValue=(114, 114, 114))

    # Visualize
    # import matplotlib.pyplot as plt
    # ax = plt.subplots(1, 2, figsize=(12, 6))[1].ravel()
    # ax[0].imshow(im[:, :, ::-1])  # base
    # ax[1].imshow(im2[:, :, ::-1])  # warped

    # Transform label coordinates
    n = len(targets)
    if n:
        # xy = np.ones((n * 4, 3))
        # xy[:, :2] = targets[:, [1, 2, 3, 4, 1, 4, 3, 2]].reshape(n * 4, 2)  # x1y1, x2y2, x1y2, x2y1
        # xy = xy @ M.T  # transform
        # xy = (xy[:, :2] / xy[:, 2:3] if perspective else xy[:, :2]).reshape(n, 8)  # perspective rescale or affine
        xy = np.ones((n * (4 + 5), 3))
        # x1y1, x2y2, x1y2, x2y1, kp1, kp2, kp3, kp4, kp5
        xy[:, :2] = (
            targets[:, [1, 2, 3, 4, 1, 4, 3, 2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]].reshape(n * 9, 2))
        xy = xy @ M.T  # transform
        xy = (xy[:, :2] / xy[:, 2:3] if perspective else xy[:, :2]).reshape(n, 18)  # perspective rescale or affine

        # create new boxes
        x = xy[:, [0, 2, 4, 6]]
        y = xy[:, [1, 3, 5, 7]]

        landmarks = xy[:, [8, 9, 10, 11, 12, 13, 14, 15, 16, 17]]
        mask_landmarks = np.array(targets[:, 5:15] > 0, dtype=np.int32)
        landmarks = landmarks * mask_landmarks
        landmarks = landmarks + mask_landmarks - 1

        landmarks = np.where(landmarks < 0, -1, landmarks)
        landmarks[:, [0, 2, 4, 6, 8]] = np.where(landmarks[:, [0, 2, 4, 6, 8]] > width, -1,
                                                 landmarks[:, [0, 2, 4, 6, 8]])
        landmarks[:, [1, 3, 5, 7, 9]] = np.where(landmarks[:, [1, 3, 5, 7, 9]] > height, -1,
                                                 landmarks[:, [1, 3, 5, 7, 9]])

        new = np.concatenate((x.min(1), y.min(1), x.max(1), y.max(1))).reshape(4, n).T
        new = np.concatenate((new, landmarks), axis=1)

        # clip
        new[:, [0, 2]] = new[:, [0, 2]].clip(0, width)
        new[:, [1, 3]] = new[:, [1, 3]].clip(0, height)

        # filter candidates
        # i = box_candidates(box1=targets[:, 1:5].T * s, box2=new.T, area_thr=0.01 if use_segments else 0.10)
        i = box_candidates(box1=targets[:, 1:5].T * s, box2=new[:, :4].T, area_thr=0.10)
        targets = targets[i]
        # targets[:, 1:5] = new[i]
        targets[:, 1:(5 + 10)] = new[i]

    return im, targets


def load_mosaic(img_path_list, labels_list, img_size=640):
    mosaic_border = [-img_size // 2, -img_size // 2]

    # YOLOv5 4-mosaic loader. Loads 1 image + 3 random images into a 4-image mosaic
    labels4 = []
    s = img_size
    yc, xc = (int(random.uniform(-x, 2 * s + x)) for x in mosaic_border)  # mosaic center x, y

    assert len(img_path_list) == len(labels_list) == 4
    for i, (img_path, labels) in enumerate(zip(img_path_list, labels_list)):
        # Load image
        img, _, (h, w) = load_image(img_path, img_size=img_size)

        # place img in img4
        if i == 0:  # top left
            img4 = np.full((s * 2, s * 2, img.shape[2]), 114, dtype=np.uint8)  # base image with 4 tiles
            x1a, y1a, x2a, y2a = max(xc - w, 0), max(yc - h, 0), xc, yc  # xmin, ymin, xmax, ymax (large image)
            x1b, y1b, x2b, y2b = w - (x2a - x1a), h - (y2a - y1a), w, h  # xmin, ymin, xmax, ymax (small image)
        elif i == 1:  # top right
            x1a, y1a, x2a, y2a = xc, max(yc - h, 0), min(xc + w, s * 2), yc
            x1b, y1b, x2b, y2b = 0, h - (y2a - y1a), min(w, x2a - x1a), h
        elif i == 2:  # bottom left
            x1a, y1a, x2a, y2a = max(xc - w, 0), yc, xc, min(s * 2, yc + h)
            x1b, y1b, x2b, y2b = w - (x2a - x1a), 0, w, min(y2a - y1a, h)
        elif i == 3:  # bottom right
            x1a, y1a, x2a, y2a = xc, yc, min(xc + w, s * 2), min(s * 2, yc + h)
            x1b, y1b, x2b, y2b = 0, 0, min(w, x2a - x1a), min(y2a - y1a, h)

        img4[y1a:y2a, x1a:x2a] = img[y1b:y2b, x1b:x2b]  # img4[ymin:ymax, xmin:xmax]
        padw = x1a - x1b
        padh = y1a - y1b

        # Labels
        if labels.size:
            # labels[:, 1:] = xywhn2xyxy(labels[:, 1:], w, h, padw, padh)  # normalized xywh to pixel xyxy format
            labels[:, 1:5] = xywhn2xyxy(labels[:, 1:5], w, h, padw, padh)  # normalized xywh to pixel xyxy format

            labels[:, 5::2] = np.where(labels[:, 5::2] < 0, -1, labels[:, 5::2] * w + padw)
            labels[:, 6::2] = np.where(labels[:, 6::2] < 0, -1, labels[:, 6::2] * h + padh)

        labels4.append(labels)

    # Concat/clip labels
    labels4 = np.concatenate(labels4, 0)
    for x in (labels4[:, 1:],):
        # np.clip(x, 0, 2 * s, out=x)  # clip when using random_perspective()
        np.clip(x[:, :4], 0, 2 * s, out=x[:, :4])  # clip when using random_perspective()

        x[:, 4::2] = np.where(x[:, 4::2] < 0, -1, x[:, 4::2])
        x[:, 4::2] = np.where(x[:, 4::2] > 2 * s, -1, x[:, 4::2])
        x[:, 5::2] = np.where(x[:, 5::2] < 0, -1, x[:, 5::2])
        x[:, 5::2] = np.where(x[:, 5::2] > 2 * s, -1, x[:, 5::2])
    # img4, labels4 = replicate(img4, labels4)  # replicate

    # Augment
    # img4, labels4, segments4 = copy_paste(img4, labels4, segments4, p=self.hyp['copy_paste'])
    img4, labels4 = random_perspective(img4,
                                       targets=labels4,
                                       degrees=0,
                                       translate=0.1,
                                       scale=0.5,
                                       shear=0,
                                       perspective=0.0,
                                       border=mosaic_border)  # border to remove

    return img4, labels4


def flip_left_right(img, labels):
    nl = len(labels)  # update after albumentations

    # Flip left-right
    img = np.fliplr(img).astype(np.uint8)
    if nl:
        labels[:, 1] = 1 - labels[:, 1]

    labels[:, 5::2] = np.where(labels[:, 5::2] < 0, -1, 1 - labels[:, 5::2])

    # 左右镜像的时候，左眼、右眼，　左嘴角、右嘴角无法区分, 应该交换位置，便于网络学习
    eye_left = np.copy(labels[:, [5, 6]])
    mouth_left = np.copy(labels[:, [11, 12]])
    labels[:, [5, 6]] = labels[:, [7, 8]]
    labels[:, [7, 8]] = eye_left
    labels[:, [11, 12]] = labels[:, [13, 14]]
    labels[:, [13, 14]] = mouth_left

    return img, labels


def do_letterbox(img_path, labels, augment=True):
    im, (h0, w0), (h, w) = load_image(img_path)
    img_shape = im.shape

    # Letterbox
    img, ratio, pad = letterbox(im, img_shape, auto=False, scaleup=augment)
    shapes = (h0, w0), ((h / h0, w / w0), pad)  # for COCO mAP rescaling

    if labels.size:  # normalized xywh to pixel xyxy format
        # labels[:, 1:] = xywhn2xyxy(labels[:, 1:], ratio[0] * w, ratio[1] * h, padw=pad[0], padh=pad[1])
        labels[:, 1:5] = xywhn2xyxy(labels[:, 1:5], ratio[0] * w, ratio[1] * h, padw=pad[0], padh=pad[1])

        labels[:, 5::2] = np.where(labels[:, 5::2] < 0, -1, labels[:, 5::2] * w + pad[0])
        labels[:, 6::2] = np.where(labels[:, 6::2] < 0, -1, labels[:, 6::2] * h + pad[1])

    return img, labels


def load_data_and_labels():
    import glob

    img_path_root = "assets/widerface_train/"
    img_path_list = sorted(glob.glob(img_path_root + "*.jpg"))
    label_path_root = "assets/widerface_train/"
    label_path_list = sorted(glob.glob(label_path_root + "*.txt"))
    assert len(img_path_list) == len(label_path_list)

    data_array = np.array([[img_path, label_path] for img_path, label_path in zip(img_path_list, label_path_list)])
    np.random.shuffle(data_array)

    img_path_list = [item[0] for item in data_array]
    label_path_list = [item[1] for item in data_array]

    img_list = []
    label_list = []
    for img_path, label_path in zip(img_path_list, label_path_list):
        label_array = np.loadtxt(label_path, dtype=float, delimiter=' ')
        if len(label_array.shape) == 1:
            label_array = label_array[np.newaxis, :]

        print(os.path.basename(img_path), label_array.shape)
        img_list.append(img_path)
        label_list.append(label_array)

    return img_list, label_list


def test_mosaic():
    # main()
    img_list, label_list = load_data_and_labels()
    print(len(img_list), len(label_list))

    print('*' * 100)
    img4, labels4 = load_mosaic(img_list, label_list, img_size=640)
    print(labels4)
    for item in labels4:
        x_min, y_min, x_max, y_max = item[1:5].astype(int)
        cv2.rectangle(img4, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

        for px, py in item[5:].reshape(-1, 2):
            if px > 0 and py > 0:
                cv2.circle(img4, (int(px), int(py)), 1, (0, 255, 0), 2)

    cv2.imshow("load_mosaic", img4)
    cv2.waitKey(0)

    cv2.imwrite("./assets/load_mosaic.jpg", img4)


def test_flip_left_right():
    # main()
    img_list, label_list = load_data_and_labels()
    print(len(img_list), len(label_list))
    img4, labels4 = load_mosaic(img_list, label_list, img_size=640)

    print('*' * 100)
    nl = len(labels4)  # number of labels
    if nl:
        labels4[:, 1:5] = xyxy2xywhn(labels4[:, 1:5], w=img4.shape[1], h=img4.shape[0], clip=True, eps=1E-3)

        # normalized landmark x 0-1
        labels4[:, 5::2] = np.where(labels4[:, 5::2] < 0, -1, labels4[:, 5::2] / img4.shape[1])
        # normalized landmark y 0-1
        labels4[:, 6::2] = np.where(labels4[:, 6::2] < 0, -1, labels4[:, 6::2] / img4.shape[0])
    print(f"img4 shape: {img4.shape} - label4 shape: {labels4.shape}")

    img_flr, labels_flr = flip_left_right(copy.deepcopy(img4), copy.deepcopy(labels4))
    print(f"img_flr shape: {img_flr.shape} - labels_flr shape: {labels_flr.shape}")

    img_h, img_w = img_flr.shape[:2]
    for item in labels_flr:
        x_c, y_c, box_w, box_h = item[1:5]
        x_min = max(1, int((x_c - box_w / 2) * img_w))
        y_min = max(1, int((y_c - box_h / 2) * img_h))
        x_max = min(int((x_c + box_w / 2) * img_w), img_w - 1)
        y_max = min(int((y_c + box_h / 2) * img_h), img_h - 1)
        print(x_min, y_min, x_max, y_max)
        cv2.rectangle(img_flr, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

        for px, py in item[5:].reshape(-1, 2):
            if px > 0 and py > 0:
                cv2.circle(img_flr, (int(px * img_w), int(py * img_h)), 1, (0, 255, 0), 2)

    cv2.imshow("flip_left_right", img_flr)
    cv2.waitKey(0)

    cv2.imwrite("./assets/flip_left_right.jpg", img_flr)


def test_letterbox():
    img_path = "./assets/widerface_train/28_Sports_Fan_Sports_Fan_28_56.jpg"
    label_path = "./assets/widerface_train/28_Sports_Fan_Sports_Fan_28_56.txt"
    labels = np.loadtxt(label_path, dtype=float, delimiter=' ')

    img, labels = do_letterbox(img_path, labels, augment=True)
    for item in labels:
        x_min, y_min, x_max, y_max = item[1:5].astype(int)
        cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

        for px, py in item[5:].reshape(-1, 2):
            if px > 0 and py > 0:
                cv2.circle(img, (int(px), int(py)), 1, (0, 255, 0), 2)

    cv2.imshow('img', img)
    cv2.waitKey(0)


if __name__ == '__main__':
    test_mosaic()
    test_flip_left_right()
    test_letterbox()
