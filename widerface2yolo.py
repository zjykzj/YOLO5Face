# -*- coding: utf-8 -*-

"""
@Time    : 2024/6/16 20:09
@File    : widerface2yolo.py
@Author  : zj
@Description:

Download the WIDERFACE dataset: http://shuoyang1213.me/WIDERFACE/

Download face and keypoint annotations: https://drive.google.com/file/d/1tU_IjyOwGQfGNUvZGwWWM4SwxKp2PUQ8/view?usp=sharing

Usage - Convert the WIDERFACE dataset format to YOLO:
    $ python3 widerface2yolo.py ../datasets/widerface/WIDER_train/images ../datasets/widerface/retinaface_gt_v1.1/train/label.txt ../datasets/widerface
    $ python3 widerface2yolo.py ../datasets/widerface/WIDER_val/images ../datasets/widerface/retinaface_gt_v1.1/val/label.txt ../datasets/widerface

"""

import os
import cv2
import shutil
import argparse

import numpy as np
from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser(description="WiderFace2YOLO")
    parser.add_argument('image', metavar='IMAGE', type=str, help='WiderFace image root.')
    parser.add_argument('label', metavar='LABEL', type=str, help='WiderFace label path.')

    parser.add_argument('dst', metavar='DST', type=str, help='YOLOLike data root.')

    args = parser.parse_args()
    print("args:", args)
    return args


def load_label(file_path, is_train=True):
    data = []
    current_image_data = None

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('#'):
                # 新的图像路径开始
                if current_image_data is not None:
                    data.append(current_image_data)
                image_path = line.strip()[2:]
                current_image_data = {'image_path': image_path, 'annotations': []}
            else:
                parts = line.split(' ')
                bbox = list(map(int, parts[:4]))
                if is_train:
                    # 从第5个元素开始，直到倒数第二个元素，每2个元素形成一个关键点
                    keypoints = [(float(parts[i]), float(parts[i + 1])) for i in range(4, len(parts) - 1, 3)]
                    assert len(keypoints) == 5, keypoints
                    confidence = float(parts[-1])
                else:
                    keypoints = [(-1.0, -1.0) for i in range(5)]
                    confidence = 0.

                annotation = {
                    'bbox': bbox,
                    'keypoints': keypoints,
                    'confidence': confidence
                }
                current_image_data['annotations'].append(annotation)

        # 添加最后一个图像的信息
        if current_image_data is not None:
            data.append(current_image_data)

    return data


def main():
    args = parse_args()

    dst_root = args.dst
    img_root = args.image
    label_path = args.label

    is_train = 'val' not in label_path
    if is_train:
        dst_img_root = os.path.join(dst_root, "images/train")
        dst_label_root = os.path.join(dst_root, "labels/train")
    else:
        dst_img_root = os.path.join(dst_root, "images/val")
        dst_label_root = os.path.join(dst_root, "labels/val")
    if not os.path.exists(dst_img_root):
        os.makedirs(dst_img_root)
    if not os.path.exists(dst_label_root):
        os.makedirs(dst_label_root)

    cls_id = 0

    assert os.path.exists(img_root), img_root
    assert os.path.exists(label_path), label_path
    print(f"Parse {label_path}")
    results = load_label(label_path, is_train=is_train)

    print(f"Processing {len(results)} images")
    for result in tqdm(results):
        image_path = os.path.join(img_root, result["image_path"])
        assert os.path.isfile(image_path), image_path

        image = cv2.imread(image_path)
        height, width, channels = image.shape

        labels = []
        for anno in result['annotations']:
            label = []

            assert isinstance(anno, dict)
            x1, y1, box_w, box_h = anno['bbox']
            x_c = 1.0 * (x1 + box_w / 2) / width
            y_c = 1.0 * (y1 + box_h / 2) / height
            box_w = 1.0 * box_w / width
            box_h = 1.0 * box_h / height
            label.extend([cls_id, x_c, y_c, box_w, box_h])

            for point in anno['keypoints']:
                x, y = point
                if x > 0:
                    x = x / width
                if y > 0:
                    y = y / height
                label.extend([x, y])

            labels.append(label)

        image_name = os.path.basename(image_path)
        dst_img_path = os.path.join(dst_img_root, image_name)
        shutil.copy(image_path, dst_img_path)

        name = os.path.splitext(image_name)[0]
        dst_label_path = os.path.join(dst_label_root, f"{name}.txt")
        np.savetxt(dst_label_path, np.array(labels), delimiter=' ', fmt='%s')


if __name__ == '__main__':
    main()
