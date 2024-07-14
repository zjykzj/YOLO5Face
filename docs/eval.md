
# EVAL

## yolov5s-v7.0 + hyp.scratch-low.yaml + e300

```shell
$ python widerface_detect.py --weights ./runs/exp2-yolov5s_v7_0-i640-e300.pt --source ../datasets/widerface/images/val/ --folder_pict ../datasets/widerface/wider_face_split/wider_face_val_bbx_gt.txt --conf-thres 0.001 --iou-thres 0.6 --save-txt --save-conf --device 0
...
YOLOv5s_v7_0 summary: 157 layers, 7039792 parameters, 0 gradients, 15.8 GFLOPs
...
Speed: 0.3ms pre-process, 9.0ms inference, 0.9ms NMS per image at shape (1, 3, 640, 640)
Results saved to runs/detect/exp4
0 labels saved to runs/detect/exp4/labels
$ cd widerface_evaluate/
$ python3 evaluation.py -p ../runs/detect/exp4/labels/ -g ./ground_truth/
Reading Predictions : 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:01<00:00, 57.64it/s]
Processing easy: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:20<00:00,  3.05it/s]
Processing medium: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:20<00:00,  3.03it/s]
Processing hard: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:20<00:00,  3.02it/s]
==================== Results ====================
Easy   Val AP: 0.9461338790996806
Medium Val AP: 0.9321276330891444
Hard   Val AP: 0.8514960494506578
=================================================
```

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

## yolov5s-face + hyp.scratch.yaml + e300

```shell
$ python widerface_detect.py --weights ./runs/exp3-yolov5s_face-i640-e300.pt --source ../datasets/widerface/images/val/ --folder_pict ../datasets/widerface/wider_face_split/wider_face_val_bbx_gt.txt --conf-thres 0.001 --iou-thres 0.6 --save-txt --save-conf --device 0
...
YOLOv5s_face summary: 171 layers, 7064992 parameters, 0 gradients, 15.2 GFLOPs
...
Speed: 0.4ms pre-process, 9.2ms inference, 0.8ms NMS per image at shape (1, 3, 640, 640)
Results saved to runs/detect/exp6
0 labels saved to runs/detect/exp6/labels
$ cd widerface_evaluate/
$ python3 evaluation.py -p ../runs/detect/exp6/labels/ -g ./ground_truth/
Reading Predictions : 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:00<00:00, 63.40it/s]
Processing easy: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:20<00:00,  3.02it/s]
Processing medium: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:19<00:00,  3.06it/s]
Processing hard: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:19<00:00,  3.07it/s]
==================== Results ====================
Easy   Val AP: 0.944292106729655
Medium Val AP: 0.9288902709524673
Hard   Val AP: 0.8509110921848383
=================================================
```

```shell
$ python widerface_detect.py --weights ./runs/exp5-yolov5s_face-i800-e300.pt --source ../datasets/widerface/images/val/ --folder_pict ../datasets/widerface/wider_face_split/wider_face_val_bbx_gt.txt --conf-thres 0.001 --iou-thres 0.6 --save-txt --save-conf --device 0
...
YOLOv5s_face summary: 171 layers, 7064992 parameters, 0 gradients, 15.2 GFLOPs
...
Speed: 0.3ms pre-process, 9.4ms inference, 0.8ms NMS per image at shape (1, 3, 640, 640)
Results saved to runs/detect/exp8
0 labels saved to runs/detect/exp8/labels
$ cd widerface_evaluate/
$ python3 evaluation.py -p ../runs/detect/exp8/labels/ -g ./ground_truth/
Reading Predictions : 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:00<00:00, 69.88it/s]
Processing easy: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:20<00:00,  3.03it/s]
Processing medium: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:19<00:00,  3.07it/s]
Processing hard: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:19<00:00,  3.08it/s]
==================== Results ====================
Easy   Val AP: 0.9469263514518231
Medium Val AP: 0.929978109599129
Hard   Val AP: 0.8472539843348216
=================================================
```