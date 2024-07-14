<div align="right">
  Language:
    🇺🇸
  <a title="Chinese" href="./README.zh-CN.md">🇨🇳</a>
</div>

<div align="center"><a title="" href="https://github.com/zjykzj/YOLO5Face"><img align="center" src="assets/logo/YOLO5Face.png" alt=""></a></div>

<p align="center">
  «YOLO5Face» reproduced the paper "YOLO5Face: Why Reinventing a Face Detector"
<br>
<br>
  <a href="https://github.com/RichardLitt/standard-readme"><img src="https://img.shields.io/badge/standard--readme-OK-green.svg?style=flat-square" alt=""></a>
  <a href="https://conventionalcommits.org"><img src="https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg" alt=""></a>
  <a href="http://commitizen.github.io/cz-cli/"><img src="https://img.shields.io/badge/commitizen-friendly-brightgreen.svg" alt=""></a>
</p>

<!-- <style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  overflow:hidden;padding:10px 5px;word-break:normal;}
.tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
.tg .tg-zkss{background-color:#FFF;border-color:inherit;color:#333;text-align:center;vertical-align:top}
.tg .tg-vc3l{background-color:#FFF;border-color:inherit;color:#1F2328;text-align:center;vertical-align:top}
.tg .tg-c3ow{border-color:inherit;text-align:center;vertical-align:top}
.tg .tg-fr9f{background-color:#FFF;border-color:inherit;color:#333;font-weight:bold;text-align:center;vertical-align:top}
.tg .tg-jw1t{background-color:#FFF;border-color:inherit;color:#555;font-weight:bold;text-align:center;vertical-align:top}
.tg .tg-7btt{border-color:inherit;font-weight:bold;text-align:center;vertical-align:top}
.tg .tg-9y4h{background-color:#FFF;border-color:inherit;color:#1F2328;text-align:center;vertical-align:middle}
.tg .tg-y5w1{background-color:#FFF;border-color:inherit;color:#00E;font-weight:bold;text-align:center;vertical-align:top}
</style> -->
<table class="tg"><thead>
  <tr>
    <th class="tg-fr9f"></th>
    <th class="tg-fr9f">ARCH</th>
    <th class="tg-fr9f">GFLOPs</th>
    <th class="tg-jw1t">Easy</th>
    <th class="tg-7btt">Medium</th>
    <th class="tg-7btt">Hard</th>
  </tr></thead>
<tbody>
  <tr>
    <td class="tg-fr9f">deepcam-cn/yolov5-face(Official)</td>
    <td class="tg-zkss"><span style="background-color:#FFF">yolov5s-face</span></td>
    <td class="tg-zkss">/</td>
    <td class="tg-9y4h">94.33</td>
    <td class="tg-9y4h">92.61</td>
    <td class="tg-9y4h">83.15</td>
  </tr>
  <tr>
    <td class="tg-y5w1">zjykzj/YOLO5Face<span style="font-weight:700;font-style:normal">(This)</span></td>
    <td class="tg-zkss"><span style="background-color:#FFF">yolov5s-face</span></td>
    <td class="tg-vc3l">15.2</td>
    <td class="tg-9y4h">94.69</td>
    <td class="tg-c3ow">93.00</td>
    <td class="tg-c3ow">84.73</td>
  </tr>
  <tr>
    <td class="tg-y5w1">zjykzj/YOLO5Face<span style="font-weight:700;font-style:normal">(This)</span></td>
    <td class="tg-zkss"><span style="background-color:#FFF">yolov5s-v7.0</span></td>
    <td class="tg-vc3l">15.8</td>
    <td class="tg-zkss">94.84</td>
    <td class="tg-vc3l">93.28</td>
    <td class="tg-vc3l">84.67</td>
  </tr>
</tbody></table>

![](./assets/results/selfie.jpg)

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Latest News](#latest-news)
- [Background](#background)
- [Installation](#installation)
- [Usage](#usage)
  - [Train](#train)
  - [Eval](#eval)
  - [Predict](#predict)
- [Maintainers](#maintainers)
- [Thanks](#thanks)
- [Contributing](#contributing)
- [License](#license)

## Latest News

* ***[2024/07/14][v1.0.0](https://github.com/zjykzj/YOLO5Face/releases/tag/v1.0.0). Add keypoint detection to achieve face+keypoint detection.***
* ***[2024/06/29][v0.1.0](https://github.com/zjykzj/YOLO5Face/releases/tag/v0.1.0). Training Face Detectors Based on YOLOv5-v7.0 and WIDERFACE Datasets.***

## Background

[YOLO5Face](https://arxiv.org/abs/2105.12931) is a very interesting work that further abstracts the task of face
detection. By directly using a universal object detection algorithm, good face detection results can be achieved. Of
course, it also achieves 5-point facial keypoint regression. Based on
the [ultralytics/yolov5](https://github.com/ultralytics/yolov5) object detection framework, YOLO5Face can easily apply
different models and training, such as using lightweight networks for real-time detection and using large networks for
higher detection accuracy.

Note: the latest implementation of YOLO5Face in our warehouse is entirely based
on [ultralytics/yolov5 v7.0](https://github.com/ultralytics/yolov5/releases/tag/v7.0)

## Installation

```shell
pip3 install -r requirements.txt
```

Or use docker container

```shell
docker run -it --runtime nvidia --gpus=all --shm-size=16g -v /etc/localtime:/etc/localtime -v $(pwd):/workdir --workdir=/workdir --name yolov2 ultralytics/yolov5:latest
```

## Usage

About dataset and annotations, see [widerface2yolo.py](./widerface2yolo.py)

### Train

```shell
# yolov5s_v7.0
$ python3 widerface_train.py --data widerface.yaml --weights "" --cfg models/yolo5face/cfgs/yolov5s_v7_0.yaml --hyp models/yolo5face/hyps/hyp.scratch-low.yaml --img 800 --epoch 300 --device 0
# yolov5s-face
$ python3 widerface_train.py --data widerface.yaml --weights "" --cfg models/yolo5face/cfgs/yolov5s_face.yaml --hyp models/yolo5face/hyps/hyp.scratch.yaml --img 800 --epoch 300 --device 0
```

### Eval

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

### Predict

```shell
$ python detect_face_and_landmarks.py --weights ./runs/exp4-yolov5s_v7_0-i800-e300.pt --source assets/selfie.jpg --imgsz 2048 --conf-thres 0.25 --iou-thres 0.45 --hide-labels --hide-conf
```

## Maintainers

* zhujian - *Initial work* - [zjykzj](https://github.com/zjykzj)

## Thanks

* [deepcam-cn/yolov5-face](https://github.com/deepcam-cn/yolov5-face)
* [ultralytics/yolov5](https://github.com/ultralytics/yolov5)
* [zjykzj/YOLOv3](https://github.com/zjykzj/YOLOv3)

## Contributing

Anyone's participation is welcome! Open an [issue](https://github.com/zjykzj/YOLO5Face/issues) or submit PRs.

Small note:

* Git submission specifications should be complied
  with [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0-beta.4/)
* If versioned, please conform to the [Semantic Versioning 2.0.0](https://semver.org) specification
* If editing the README, please conform to the [standard-readme](https://github.com/RichardLitt/standard-readme)
  specification.

## License

[Apache License 2.0](LICENSE) © 2024 zjykzj