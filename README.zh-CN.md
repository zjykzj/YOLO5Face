<div align="right">
  语言:
    🇨🇳
  <a title="英语" href="./README.md">🇺🇸</a>
</div>

<div align="center"><a title="" href="https://github.com/zjykzj/YOLO5Face"><img align="center" src="assets/logo/YOLO5Face.png" alt=""></a></div>

<p align="center">
  «YOLO5Face» 复现了论文 "YOLO5Face: Why Reinventing a Face Detector"
<br>
<br>
  <a href="https://github.com/RichardLitt/standard-readme"><img src="https://img.shields.io/badge/standard--readme-OK-green.svg?style=flat-square" alt=""></a>
  <a href="https://conventionalcommits.org"><img src="https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg" alt=""></a>
  <a href="http://commitizen.github.io/cz-cli/"><img src="https://img.shields.io/badge/commitizen-friendly-brightgreen.svg" alt=""></a>
</p>

|                                      |       ARCH        | GFLOPs |   Easy    |  Medium   |   Hard    |
|:------------------------------------:|:-----------------:|:------:|:---------:|:---------:|:---------:|
|     **zjykzj/YOLO5Face (This)**      |   yolov5s-face    |  15.2  |   94.69   |   93.00   |   84.73   |
| **deepcam-cn/yolov5-face(Official)** |   yolov5s-face    |   /    |   94.33   |   92.61   |   83.15   |
|     **zjykzj/YOLO5Face (This)**      | shufflenetv2-face |  1.5   |   90.27   |   87.39   |   73.60   |
| **deepcam-cn/yolov5-face(Official)** | shufflenetv2-face |   /    |   90.76   |   88.12   |   73.82   |
|                                      |                   |        |           |           |           |
|     **zjykzj/YOLO5Face (This)**      |   yolov5x-v7.0    |  204   | **95.79** | **94.53** | **87.63** |
|     **zjykzj/YOLO5Face (This)**      |   yolov5s-v7.0    |  15.8  |   94.84   |   93.28   |   84.67   |
|     **zjykzj/YOLO5Face (This)**      |   yolov5n-v7.0    |  4.2   |   93.25   |   91.11   |   80.33   |

![](./assets/results/selfie.jpg)

## 内容列表

- [内容列表](#内容列表)
- [新闻🚀🚀🚀](#新闻)
- [背景](#背景)
- [安装](#安装)
- [用法](#用法)
  - [训练](#训练)
  - [评估](#评估)
  - [预测](#预测)
- [主要维护人员](#主要维护人员)
- [致谢](#致谢)
- [参与贡献方式](#参与贡献方式)
- [许可证](#许可证)

## 新闻🚀🚀🚀

| 版本                                                                | 发布日期       | 主要更新                                                  |
|-------------------------------------------------------------------|------------|-------------------------------------------------------|
| [v1.1.0](https://github.com/zjykzj/YOLO5Face/releases/tag/v1.1.0) | 2024/07/21 | 支持更多模型，包括shufflenetv2-face/yolov5x-v7.0/yolov5n-v7.0。 |
| [v1.0.0](https://github.com/zjykzj/YOLO5Face/releases/tag/v1.0.0) | 2024/07/14 | 增加关键点检测，实现人脸+关键点检测。                                   |
| [v0.1.0](https://github.com/zjykzj/YOLO5Face/releases/tag/v0.1.0) | 2024/06/29 | 基于yolov5-v7.0和WIDERFACE数据集训练人脸检测器。                    |

## 背景

[YOLO5Face](https://arxiv.org/abs/2105.12931)是一个很有趣的工作，它进一步抽象了人脸检测任务，直接采用通用目标检测算法就可以实现很好的人脸检测效果。当然它还实现了5点人脸关键点回归。 基于[ultralytics/yolov5](https://github.com/ultralytics/yolov5)，YOLO5Face可以很方便的应用不同的模型和训练，比如采用轻量网络来实现实时检测，采用大网络来实现更高的检测精度。

注意：当前本仓库最新的实现完全基于[ultralytics/yolov5 v7.0](https://github.com/ultralytics/yolov5/releases/tag/v7.0)

## 安装

```shell
pip3 install -r requirements.txt
```

或者使用Docker Container

```shell
docker run -it --runtime nvidia --gpus=all --shm-size=16g -v /etc/localtime:/etc/localtime -v $(pwd):/workdir --workdir=/workdir --name yolo5face ultralytics/yolov5:latest
```

## 用法

下载WIDERFACE数据集：[Baidu Drive](https://pan.baidu.com/s/1aHdWgLq1ne_MEr9fkcS7Rg)(08p0)

### 训练

```shell
# yolov5s_v7.0
$ python3 widerface_train.py --data widerface.yaml --weights "" --cfg models/yolo5face/cfgs/yolov5s_v7_0.yaml --hyp models/yolo5face/hyps/hyp.scratch-low.yaml --img 800 --epoch 300 --device 0
# yolov5s-face
$ python3 widerface_train.py --data widerface.yaml --weights "" --cfg models/yolo5face/cfgs/yolov5s_face.yaml --hyp models/yolo5face/hyps/hyp.scratch.yaml --img 800 --epoch 300 --device 0
```

### 评估

```shell
$ python widerface_detect.py --weights ./runs/exp4-yolov5s_v7_0-i800-e300.pt --source ../datasets/widerface/images/val/ --folder_pict ../datasets/widerface/wider_face_split/wider_face_val_bbx_gt.txt --conf-thres 0.001 --iou-thres 0.6 --save-txt --save-conf --device 0
...
YOLOv5s_v7_0 summary: 157 layers, 7039792 parameters, 0 gradients, 15.8 GFLOPs
...
Speed: 0.4ms pre-process, 8.8ms inference, 0.8ms NMS per image at shape (1, 3, 640, 640)
Results saved to runs/detect/exp7
0 labels saved to runs/detect/exp7/labels
$ cd widerface_evaluate/
$ python3 evaluation.py -p ../runs/detect/exp7/labels/ -g ./ground_truth/
Reading Predictions : 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:00<00:00, 62.18it/s]
Processing easy: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:20<00:00,  2.94it/s]
Processing medium: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:20<00:00,  2.98it/s]
Processing hard: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:20<00:00,  2.97it/s]
==================== Results ====================
Easy   Val AP: 0.9483604102331251
Medium Val AP: 0.9328484206418773
Hard   Val AP: 0.8467345083774318
=================================================
```

### 预测

```shell
$ python detect_face_and_landmarks.py --weights ./runs/exp4-yolov5s_v7_0-i800-e300.pt --source assets/selfie.jpg --imgsz 2048 --conf-thres 0.25 --iou-thres 0.45 --hide-labels --hide-conf
```

## 主要维护人员

* zhujian - *Initial work* - [zjykzj](https://github.com/zjykzj)

## 致谢

* [zjykzj/YOLOv3](https://github.com/zjykzj/YOLOv3)
* [ultralytics/yolov5](https://github.com/ultralytics/yolov5)
* [deepcam-cn/yolov5-face](https://github.com/deepcam-cn/yolov5-face)
* [WIDER FACE: A Face Detection Benchmark](http://shuoyang1213.me/WIDERFACE/)

## 参与贡献方式

欢迎任何人的参与！打开[issue](https://github.com/zjykzj/YOLO5Face/issues)或提交合并请求。

注意:

* `GIT`提交，请遵守[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0-beta.4/)规范
* 语义版本化，请遵守[Semantic Versioning 2.0.0](https://semver.org)规范
* `README`编写，请遵守[standard-readme](https://github.com/RichardLitt/standard-readme)规范

## 许可证

[Apache License 2.0](LICENSE) © 2024 zjykzj