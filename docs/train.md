
# TRAIN

* Dataset
  * Train: `WDIER_train (12876)`
  * Val: `WIDER_val (3226)`
* Epoches: `300`
* Model
  * Set1: `yolov5s-face (Official)`
  * Set5: `shufflenetv2-face (Official)`
  * Set4: `yolov5x-v7.0 (Custom Face+Keypoints)`
  * Set2: `yolov5s-v7.0 (Custom Face+Keypoints)`
  * Set3: `yolov5n-v7.0 (Custom Face+Keypoints)`
* ImgSZ
  * Set1: `640`
  * Set2: `800`
* Hyp
  * Set1: `hyp.scratch.yaml (Official)`
  * Set2: `hyp.scratch-low.yaml (From yolov5-v7.0)`

## yolov5s-face + hyp.scratch.yaml + e300

### img640

```shell
$ python3 widerface_train.py --data widerface.yaml --weights "" --cfg models/yolo5face/cfgs/yolov5s_face.yaml --hyp models/yolo5face/hyps/hyp.scratch.yaml --img 640 --epoch 300 --device 0
         Epoch       GPU_mem      box_loss      obj_loss      cls_loss landmark_loss     Instances          Size
       299/299         9.23G        0.0414       0.02934             0      0.007429           217           640: 100%|██████████| 805/805 01:40
                       Class        Images     Instances             P             R         mAP50      mAP50-95: 100%|██████████| 101/101 00:18
                         all          3226         39707         0.865         0.666         0.737         0.394

300 epochs completed in 9.661 hours.
Optimizer stripped from runs/train/exp3/weights/last.pt, 14.5MB
Optimizer stripped from runs/train/exp3/weights/best.pt, 14.5MB

Validating runs/train/exp3/weights/best.pt...
Fusing layers...
YOLOv5s_face summary: 171 layers, 7064992 parameters, 0 gradients, 15.2 GFLOPs
                       Class        Images     Instances             P             R         mAP50      mAP50-95: 100%|██████████| 101/101 00:33
                         all          3226         39707         0.865         0.666         0.737         0.394
Results saved to runs/train/exp3
```

### img800

```shell
$ python3 widerface_train.py --data widerface.yaml --weights "" --cfg models/yolo5face/cfgs/yolov5s_face.yaml --hyp models/yolo5face/hyps/hyp.scratch.yaml --img 800 --epoch 300 --device 0
         Epoch       GPU_mem      box_loss      obj_loss      cls_loss landmark_loss     Instances          Size
       299/299           13G       0.03926       0.03324             0       0.00747           217           800: 100%|██████████| 805/805 01:53
                       Class        Images     Instances             P             R         mAP50      mAP50-95: 100%|██████████| 101/101 00:18
                         all          3226         39707         0.871         0.707         0.783         0.421

300 epochs completed in 11.394 hours.
Optimizer stripped from runs/train/exp5/weights/last.pt, 14.5MB
Optimizer stripped from runs/train/exp5/weights/best.pt, 14.5MB

Validating runs/train/exp5/weights/best.pt...
Fusing layers...
YOLOv5s_face summary: 171 layers, 7064992 parameters, 0 gradients, 15.2 GFLOPs
                       Class        Images     Instances             P             R         mAP50      mAP50-95: 100%|██████████| 101/101 00:33
                         all          3226         39707          0.87         0.707         0.783         0.421
Results saved to runs/train/exp5
```

## shufflev2-face + hyp.scratch-low.yaml + e300 + img800

```shell
$ python3 widerface_train.py --data widerface.yaml --weights "" --cfg models/yolo5face/cfgs/shufflev2-face.yaml --hyp models/yolo5face/hyps/hyp.scratch-low.yaml --img 800 --epoch 300 --device 0
         Epoch       GPU_mem      box_loss      obj_loss      cls_loss landmark_loss     Instances          Size
       299/299          6.6G       0.05001       0.04768             0       0.08396           164           800: 100%|██████████| 805/805 01:44
                       Class        Images     Instances             P             R         mAP50      mAP50-95: 100%|██████████| 101/101 00:17
                         all          3226         39707         0.841         0.584         0.666         0.334

300 epochs completed in 10.457 hours.
Optimizer stripped from runs/train/exp/weights/last.pt, 1.3MB
Optimizer stripped from runs/train/exp/weights/best.pt, 1.3MB

Validating runs/train/exp/weights/best.pt...
Fusing layers...
shufflev2-face summary: 278 layers, 446376 parameters, 0 gradients, 1.5 GFLOPs
                       Class        Images     Instances             P             R         mAP50      mAP50-95: 100%|██████████| 101/101 00:29
                         all          3226         39707         0.841         0.584         0.666         0.334
Results saved to runs/train/exp
```

## yolov5x-v7.0 + hyp.scratch-low.yaml + e300 + img800

```shell
$ python3 widerface_train.py --data widerface.yaml --weights "" --cfg models/yolo5face/cfgs/yolov5x_v7_0.yaml --hyp models/yolo5face/hyps/hyp.scratch-low.yaml --img 800 --epoch 300 --device 0
         Epoch       GPU_mem      box_loss      obj_loss      cls_loss landmark_loss     Instances          Size
       299/299         22.2G       0.04602       0.04323             0       0.05141           164           800: 100%|██████████| 805/805 08:14
                       Class        Images     Instances             P             R         mAP50      mAP50-95: 100%|██████████| 101/101 00:39
                         all          3226         39707         0.896         0.733         0.812         0.447

300 epochs completed in 44.796 hours.
Optimizer stripped from runs/train/exp3/weights/last.pt, 173.2MB
Optimizer stripped from runs/train/exp3/weights/best.pt, 173.2MB

Validating runs/train/exp3/weights/best.pt...
Fusing layers...
YOLOv5x_v7_0 summary: 322 layers, 86240704 parameters, 0 gradients, 204.0 GFLOPs
                       Class        Images     Instances             P             R         mAP50      mAP50-95: 100%|██████████| 101/101 00:56
                         all          3226         39707         0.896         0.733         0.812         0.447
Results saved to runs/train/exp3
```

## yolov5s-v7.0 + hyp.scratch-low.yaml + e300

### img640

```shell
$ python3 widerface_train.py --data widerface.yaml --weights "" --cfg models/yolo5face/cfgs/yolov5s_v7_0.yaml --hyp models/yolo5face/hyps/hyp.scratch-low.yaml --img 640 --epoch 300 --device 0
         Epoch       GPU_mem      box_loss      obj_loss      cls_loss landmark_loss     Instances          Size
       299/299         8.23G       0.05357       0.04102             0       0.06363           164           640: 100%|██████████| 805/805 01:38
                       Class        Images     Instances             P             R         mAP50      mAP50-95: 100%|██████████| 101/101 00:18
                         all          3226         39707         0.872         0.668         0.737         0.392

300 epochs completed in 9.393 hours.
Optimizer stripped from runs/train/exp2/weights/last.pt, 14.4MB
Optimizer stripped from runs/train/exp2/weights/best.pt, 14.4MB

Validating runs/train/exp2/weights/best.pt...
Fusing layers...
YOLOv5s_v7_0 summary: 157 layers, 7039792 parameters, 0 gradients, 15.8 GFLOPs
                       Class        Images     Instances             P             R         mAP50      mAP50-95: 100%|██████████| 101/101 00:33
                         all          3226         39707         0.871         0.668         0.737         0.393
Results saved to runs/train/exp2
```

### img800

```shell
$ python3 widerface_train.py --data widerface.yaml --weights "" --cfg models/yolo5face/cfgs/yolov5s_v7_0.yaml --hyp models/yolo5face/hyps/hyp.scratch-low.yaml --img 800 --epoch 300 --device 0
         Epoch       GPU_mem      box_loss      obj_loss      cls_loss landmark_loss     Instances          Size
       299/299         11.1G       0.05043       0.04629             0        0.0605           164           800: 100%|██████████| 805/805 01:52
                       Class        Images     Instances             P             R         mAP50      mAP50-95: 100%|██████████| 101/101 00:18
                         all          3226         39707         0.879         0.704         0.781         0.419

300 epochs completed in 11.094 hours.
Optimizer stripped from runs/train/exp4/weights/last.pt, 14.5MB
Optimizer stripped from runs/train/exp4/weights/best.pt, 14.5MB

Validating runs/train/exp4/weights/best.pt...
Fusing layers...
YOLOv5s_v7_0 summary: 157 layers, 7039792 parameters, 0 gradients, 15.8 GFLOPs
                       Class        Images     Instances             P             R         mAP50      mAP50-95: 100%|██████████| 101/101 00:34
                         all          3226         39707         0.881         0.704         0.781         0.419
Results saved to runs/train/exp4
```

## yolov5n-v7.0 + hyp.scratch-low.yaml + e300 + img800

### From Scratch

```shell
$ python3 widerface_train.py --data widerface.yaml --weights "" --cfg models/yolo5face/cfgs/yolov5n_v7_0.yaml --hyp models/yolo5face/hyps/hyp.scratch-low.yaml --img 800 --epoch 300 --device 0
         Epoch       GPU_mem      box_loss      obj_loss      cls_loss landmark_loss     Instances          Size
       299/299         7.19G       0.05598       0.05071             0       0.07276           164           800: 100%|██████████| 805/805 01:36
                       Class        Images     Instances             P             R         mAP50      mAP50-95: 100%|██████████| 101/101 00:18
                         all          3226         39707         0.869         0.653         0.733         0.381

300 epochs completed in 9.713 hours.
Optimizer stripped from runs/train/exp2/weights/last.pt, 3.9MB
Optimizer stripped from runs/train/exp2/weights/best.pt, 3.9MB

Validating runs/train/exp2/weights/best.pt...
Fusing layers...
YOLOv5n_v7_0 summary: 157 layers, 1774048 parameters, 0 gradients, 4.2 GFLOPs
                       Class        Images     Instances             P             R         mAP50      mAP50-95: 100%|██████████| 101/101 00:36
                         all          3226         39707         0.869         0.652         0.733         0.381
Results saved to runs/train/exp2
```

### COCO Pretrained

```shell
$ python3 widerface_train.py --data widerface.yaml --weights yolov5n.pt --cfg models/yolo5face/cfgs/yolov5n_v7_0.yaml --hyp models/yolo5face/hyps/hyp.scratch-low.yaml --img 800 --epoch 300 --device 0
         Epoch       GPU_mem      box_loss      obj_loss      cls_loss landmark_loss     Instances          Size
       299/299         5.02G         0.055       0.04921             0       0.07114           164           800: 100%|██████████| 805/805 01:37
                       Class        Images     Instances             P             R         mAP50      mAP50-95: 100%|██████████| 101/101 00:17
                         all          3226         39707         0.864         0.659         0.736         0.383

300 epochs completed in 9.561 hours.
Optimizer stripped from runs/train/exp5/weights/last.pt, 3.9MB
Optimizer stripped from runs/train/exp5/weights/best.pt, 3.9MB

Validating runs/train/exp5/weights/best.pt...
Fusing layers...
YOLOv5n_v7_0 summary: 157 layers, 1774048 parameters, 0 gradients, 4.2 GFLOPs
                       Class        Images     Instances             P             R         mAP50      mAP50-95: 100%|██████████| 101/101 00:31
                         all          3226         39707         0.864         0.659         0.736         0.384
Results saved to runs/train/exp5
```