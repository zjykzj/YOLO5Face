
# TRAIN

## Different ImgSZ (640 vs. 800) and EPOCHs (100 vs. 250)

The training data uses `WDIER_train (12876)`, the validation data uses `WIDER_val (3226)`, and the training configuration defaults to `yolov5-v7.0` settings. Only the image size `--imgsz` and number of training rounds `--epochs` are modified.

```shell
python3 train.py --data widerface.yaml --weights yolov5s.pt --cfg yolov5s.yaml --imgsz 640 --epoch 100 --device 0
      Epoch    GPU_mem   box_loss   obj_loss   cls_loss  Instances       Size
      99/99      6.21G    0.04907    0.03883          0        241        640: 100%|██████████| 805/805 01:32
                 Class     Images  Instances          P          R      mAP50   mAP50-95: 100%|██████████| 101/101 00:17
                   all       3225      39675      0.863      0.656      0.725      0.392

100 epochs completed in 3.085 hours.
Optimizer stripped from runs/train/exp2/weights/last.pt, 14.4MB
Optimizer stripped from runs/train/exp2/weights/best.pt, 14.4MB

Validating runs/train/exp2/weights/best.pt...
Fusing layers...
YOLOv5s summary: 157 layers, 7012822 parameters, 0 gradients, 15.8 GFLOPs
                 Class     Images  Instances          P          R      mAP50   mAP50-95: 100%|██████████| 101/101 00:30
                   all       3225      39675      0.864      0.655      0.725      0.392
Results saved to runs/train/exp2
```

```shell
python3 train.py --data widerface.yaml --weights yolov5s.pt --cfg yolov5s.yaml --imgsz 640 --epoch 250 --device 0
      Epoch    GPU_mem   box_loss   obj_loss   cls_loss  Instances       Size
    249/249      6.21G    0.04587      0.037          0         99        640: 100%|██████████| 805/805 01:33
                 Class     Images  Instances          P          R      mAP50   mAP50-95: 100%|██████████| 101/101 00:17
                   all       3225      39675      0.875      0.661      0.736      0.398

250 epochs completed in 7.720 hours.
Optimizer stripped from runs/train/exp3/weights/last.pt, 14.4MB
Optimizer stripped from runs/train/exp3/weights/best.pt, 14.4MB

Validating runs/train/exp3/weights/best.pt...
Fusing layers...
YOLOv5s summary: 157 layers, 7012822 parameters, 0 gradients, 15.8 GFLOPs
                 Class     Images  Instances          P          R      mAP50   mAP50-95: 100%|██████████| 101/101 00:31
                   all       3225      39675      0.876      0.661      0.736      0.398
Results saved to runs/train/exp3
```

```shell
python3 train.py --data widerface.yaml --weights yolov5s.pt --cfg yolov5s.yaml --imgsz 800 --epoch 250 --device 0
      Epoch    GPU_mem   box_loss   obj_loss   cls_loss  Instances       Size
    249/249      9.45G    0.02695    0.03435          0         99        800: 100%|██████████| 805/805 01:45
                 Class     Images  Instances          P          R      mAP50   mAP50-95: 100%|██████████| 101/101 00:18
                   all       3225      39675      0.881      0.686      0.762      0.417

250 epochs completed in 8.922 hours.
Optimizer stripped from runs/train/exp4/weights/last.pt, 14.4MB
Optimizer stripped from runs/train/exp4/weights/best.pt, 14.4MB

Validating runs/train/exp4/weights/best.pt...
Fusing layers...
YOLOv5s summary: 157 layers, 7012822 parameters, 0 gradients, 15.8 GFLOPs
                 Class     Images  Instances          P          R      mAP50   mAP50-95: 100%|██████████| 101/101 00:32
                   all       3225      39675       0.88      0.689      0.762      0.419
Results saved to runs/train/exp4
```

## YOLOv5s vs. YOLOv5s-face

Using the yolov5s-face model and training settings of [deepcam-cn/yolov5-face](https://github.com/deepcam-cn/yolov5-face), set the input size to `800` and the number of training rounds to `250`.

```shell
python3 train.py --data widerface.yaml --weights '' --cfg models/yolo5face/cfgs/yolov5s_face.yaml --hyp models/yolo5face/hyp.scratch.yaml --img 800 --epoch 250 --device 0
      Epoch    GPU_mem   box_loss   obj_loss   cls_loss  Instances       Size
    249/249      11.3G    0.03976    0.03438          0        158        800: 100%|██████████| 805/805 01:53
                 Class     Images  Instances          P          R      mAP50   mAP50-95: 100%|██████████| 101/101 00:19
                   all       3225      39675      0.879      0.689      0.764      0.419

250 epochs completed in 9.245 hours.
Optimizer stripped from runs/train/exp/weights/last.pt, 14.5MB
Optimizer stripped from runs/train/exp/weights/best.pt, 14.5MB

Validating runs/train/exp/weights/best.pt...
Fusing layers...
YOLOv5s_face summary: 171 layers, 7038022 parameters, 0 gradients, 15.1 GFLOPs
                 Class     Images  Instances          P          R      mAP50   mAP50-95: 100%|██████████| 101/101 00:33
                   all       3225      39675      0.879      0.689      0.764      0.419
Results saved to runs/train/exp
```
