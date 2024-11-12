
# SPPF (k=3 vs. k=5)

From the experimental results, it can be seen that the training effects of setting `SPPF(k=3)` and setting `SPPF(k=5)` are similar.

| Model                  | Easy Val AP | Medium Val AP | Hard Val AP |
|------------------------| ----------- | ------------- | ----------- |
| YOLOv5n with SPPF(k=5) | 0.92797     | 0.90772       | 0.80272     |
| YOLOv5n with SPPF(k=3) | 0.92628     | 0.90603       | 0.80403     |

## yolov5n-v7.0 with SPPF(k=5) + hyp.scratch-low.yaml + e300 + img800

### Train

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

### Eval

```shell
$ python widerface_detect.py --weights ./runs/exp2-yolov5n_v7_0_from_scratch-i800-e300.pt --source ../datasets/widerface/images/val/ --folder_pict ../datasets/widerface/wider_face_split/wider_face_val_bbx_gt.txt --conf-thres 0.001 --iou-thres 0.6 --save-txt --save-conf --device 0
...
YOLOv5n_v7_0 summary: 157 layers, 1774048 parameters, 0 gradients, 4.2 GFLOPs
...
Speed: 0.4ms pre-process, 9.7ms inference, 1.1ms NMS per image at shape (1, 3, 640, 640)
Results saved to runs/detect/exp
$ cd widerface_evaluate/
$ python3 evaluation.py -p ../runs/detect/exp/labels/ -g ./ground_truth/
...
...
==================== Results ====================
Easy   Val AP: 0.9279693210456833
Medium Val AP: 0.9077221265645521
Hard   Val AP: 0.8027201542745954
=================================================
```

## yolov5n-v7.0 with SPPF(k=3) + hyp.scratch-low.yaml + e300 + img800

### Train

```shell
$ python3 widerface_train.py --data widerface.yaml --weights "" --cfg models/yolo5face/cfgs/yolov5n_v7_0.yaml --hyp models/yolo5face/hyps/hyp.scratch-low.yaml --img 800 --epoch 300 --device 0
         Epoch       GPU_mem      box_loss      obj_loss      cls_loss landmark_loss     Instances          Size
       299/299            6G       0.05603       0.05023             0       0.07301           163           800: 100%|██████████| 805/805 01:51
                       Class        Images     Instances             P             R         mAP50      mAP50-95: 100%|██████████| 101/101 00:19
                         all          3226         39707         0.866         0.654         0.735         0.381

300 epochs completed in 11.031 hours.
Optimizer stripped from runs/train/exp2/weights/last.pt, 3.9MB
Optimizer stripped from runs/train/exp2/weights/best.pt, 3.9MB

Validating runs/train/exp2/weights/best.pt...
Fusing layers...
YOLOv5n_v7_0 summary: 157 layers, 1774048 parameters, 0 gradients, 4.2 GFLOPs
                       Class        Images     Instances             P             R         mAP50      mAP50-95: 100%|██████████| 101/101 00:33
                         all          3226         39707         0.866         0.654         0.735         0.382
Results saved to runs/train/exp2
```

### Eval

```shell
$ python widerface_detect.py --weights ./runs/train/exp2/weights/best.pt --source ../datasets/widerface/images/val/ --folder_pict ../datasets/widerface/wider_face_split/wider_face_val_bbx_gt.txt --conf-thres 0.001 --iou-thres 0.6 --save-txt --save-conf --device 0
...
YOLOv5n_v7_0 summary: 157 layers, 1774048 parameters, 0 gradients, 4.2 GFLOPs
...
Speed: 0.3ms pre-process, 6.1ms inference, 1.0ms NMS per image at shape (1, 3, 640, 640)
Results saved to runs/detect/exp
$ cd widerface_evaluate/
$ python3 evaluation.py -p ../runs/detect/exp/labels/ -g ./ground_truth/
...
...
==================== Results ====================
Easy   Val AP: 0.9262807230886898
Medium Val AP: 0.9060271138515668
Hard   Val AP: 0.8040277054176698
=================================================
```

