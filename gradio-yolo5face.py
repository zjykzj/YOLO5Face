# -*- coding: utf-8 -*-

"""
@date: 2024/8/17 下午8:17
@file: gradio-yolo5face.py
@author: zj
@description: 
"""

import os
import sys
import glob
from pathlib import Path
from datetime import datetime

import gradio as gr
import numpy as np
import torch

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from models.common import DetectMultiBackend
from utils.general import LOGGER, Profile, check_img_size, cv2, scale_boxes
from utils.plots import Annotator, colors
from utils.torch_utils import select_device, smart_inference_mode
from utils.augmentations import letterbox

from models.yolo5face.general import non_max_suppression, scale_landmarks

save_root = "./runs/"
if not os.path.exists(save_root):
    os.makedirs(save_root)

# Model
device = torch.device("cpu")
model = DetectMultiBackend("./shufflev2_face-i800-e300.onnx", device=device, dnn=False, data=None, fp16=False)
imgsz = (640, 640)
model.warmup(imgsz=(1, 3, *imgsz))  # warmup


@smart_inference_mode()
def run(
        im0,
        model,
        imgsz=(640, 640),  # inference size (height, width)
        conf_thres=0.25,  # confidence threshold
        iou_thres=0.45,  # NMS IOU threshold
        max_det=1000,  # maximum detections per image
        classes=None,  # filter by class: --class 0, or --class 0 2 3
        agnostic_nms=False,  # class-agnostic NMS
        line_thickness=3,  # bounding box thickness (pixels)
):
    # Load model
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz, s=stride)  # check image size

    # Run inference
    seen, windows, dt = 0, [], (Profile(), Profile(), Profile())

    img_size = 640
    stride = 32
    auto = False
    im = letterbox(im0, img_size, stride=stride, auto=auto)[0]  # padded resize
    im = im.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
    im = np.ascontiguousarray(im)  # contiguous

    with dt[0]:
        im = torch.from_numpy(im).to(model.device)
        im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim

    # Inference
    with dt[1]:
        pred = model(im, augment=False, visualize=False)

    # NMS
    with dt[2]:
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)

    # Second-stage classifier (optional)
    # pred = utils.general.apply_classifier(pred, classifier_model, im, im0s)

    # Process predictions
    for i, det in enumerate(pred):  # per image
        seen += 1

        annotator = Annotator(im0, line_width=line_thickness, example=str(names), use_cv2=True)
        if len(det):
            # Rescale boxes from img_size to im0 size
            det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()
            det[:, 6:] = scale_landmarks(im.shape[2:], det[:, 6:], im0.shape).round()

            # Write results
            # for *xyxy, conf, cls in reversed(det):
            for item in reversed(det):
                xyxy, conf, cls, landmarks = item[:4], item[4], item[5], item[6:]

                c = int(cls)  # integer class
                # label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                # annotator.box_label(xyxy, label, color=colors(c, True))
                annotator.box_label(xyxy, label="", landmarks=landmarks, color=colors(c, True))

        # Stream results
        im0 = annotator.result()

    # Print results
    t = tuple(x.t / seen * 1E3 for x in dt)  # speeds per image
    LOGGER.info(f'Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS per image at shape {(1, 3, *imgsz)}' % t)

    return im0


def predict(inp):
    # 获取当前日期和时间
    now = datetime.now()
    # 格式化为字符串，例如 "2024-08-16_21-37-00"
    formatted_time = now.strftime("%Y-%m-%d_%H-%M-%S")
    inp.save(os.path.join(save_root, f"{formatted_time}.jpg"))

    image = np.array(inp)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    image = run(image, model)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


if __name__ == '__main__':
    gr.Interface(fn=predict,
                 inputs=gr.Image(type="pil"),
                 outputs="image",
                 examples=list(glob.glob("./assets/widerface/*.jpg"))).launch()
