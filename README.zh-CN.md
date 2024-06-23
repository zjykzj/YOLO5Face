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

## 内容列表

- [内容列表](#内容列表)
- [背景](#背景)
- [主要维护人员](#主要维护人员)
- [致谢](#致谢)
- [参与贡献方式](#参与贡献方式)
- [许可证](#许可证)

## 背景

[YOLO5Face](https://arxiv.org/abs/2105.12931)是一个很有趣的工作，它进一步抽象了人脸检测任务，直接采用通用目标检测算法就可以实现很好的人脸检测效果。当然它还实现了5点人脸关键点回归。 基于[ultralytics/yolov5](https://github.com/ultralytics/yolov5)目标检测框架，YOLO5Face可以很方便的应用不同的模型和训练，比如采用轻量网络来实现实时检测，采用大网络来实现更高的检测精度。

注意：当前本仓库最新的实现完全基于[ultralytics/yolov5 v7.0](https://github.com/ultralytics/yolov5/releases/tag/v7.0)

## 主要维护人员

* zhujian - *Initial work* - [zjykzj](https://github.com/zjykzj)

## 致谢

* [deepcam-cn/yolov5-face](https://github.com/deepcam-cn/yolov5-face)
* [ultralytics/yolov5](https://github.com/ultralytics/yolov5)
* [zjykzj/YOLOv3](https://github.com/zjykzj/YOLOv3)

## 参与贡献方式

欢迎任何人的参与！打开[issue](https://github.com/zjykzj/YOLO5Face/issues)或提交合并请求。

注意:

* `GIT`提交，请遵守[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0-beta.4/)规范
* 语义版本化，请遵守[Semantic Versioning 2.0.0](https://semver.org)规范
* `README`编写，请遵守[standard-readme](https://github.com/RichardLitt/standard-readme)规范

## 许可证

[Apache License 2.0](LICENSE) © 2024 zjykzj