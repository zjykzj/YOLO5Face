
# EVAL

Try different combinations of confidence thresholds `--conf-thres` and IOU thresholds `--iou-thres` to evaluate performance on the `WDIER_val` dataset.

1. `0.25 0.45` (detect.py)
2. `0.001 0.6` (val.py)
3. `0.02 0.5` (official test_widerface.py)

***Note: maximum detections per image is 1000 here***

## YOLOv5s

```shell
# python widerface_detect.py --weights ./runs/train/exp4-yolov5s-e250-img800.pt --source ../datasets/widerface/images/val/ --folder_pict ../datasets/widerface/wider_face_split/wider_face_val_bbx_gt.txt --conf-thres 0.25 --iou-thres 0.45 --save-txt --save-conf --device 0
...
YOLOv5s summary: 157 layers, 7012822 parameters, 0 gradients, 15.8 GFLOPs
...
Speed: 0.4ms pre-process, 8.7ms inference, 0.8ms NMS per image at shape (1, 3, 640, 640)
Results saved to runs/detect/exp4
0 labels saved to runs/detect/exp4/labels
# cd widerface_evaluate/
# python3 evaluation.py -p ../runs/detect/exp4/labels/ -g ./ground_truth/
Reading Predictions : 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:00<00:00, 364.92it/s]
Processing easy: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:17<00:00,  3.51it/s]
Processing medium: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:17<00:00,  3.52it/s]
Processing hard: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:17<00:00,  3.52it/s]
==================== Results ====================
Easy   Val AP: 0.9463598577400709
Medium Val AP: 0.9197101476218299
Hard   Val AP: 0.7863305381914243
=================================================
```

```shell
# python widerface_detect.py --weights ./runs/train/exp4-yolov5s-e250-img800.pt --source ../datasets/widerface/images/val/ --folder_pict ../datasets/widerface/wider_face_split/wider_face_val_bbx_gt.txt --conf-thres 0.001 --iou-thres 0.6 --save-txt --save-conf --device 0
...
YOLOv5s summary: 157 layers, 7012822 parameters, 0 gradients, 15.8 GFLOPs
...
Speed: 0.3ms pre-process, 9.0ms inference, 0.9ms NMS per image at shape (1, 3, 640, 640)
Results saved to runs/detect/exp5
0 labels saved to runs/detect/exp5/labels
# cd widerface_evaluate/
# python3 evaluation.py -p ../runs/detect/exp5/labels/ -g ./ground_truth/
Reading Predictions : 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:00<00:00, 94.45it/s]
Processing easy: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:19<00:00,  3.13it/s]
Processing medium: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:19<00:00,  3.12it/s]
Processing hard: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:19<00:00,  3.13it/s]
==================== Results ====================
Easy   Val AP: 0.9520941964576021
Medium Val AP: 0.9341770033021547
Hard   Val AP: 0.8403303849682994
=================================================
```

```shell
# python widerface_detect.py --weights ./runs/train/exp4-yolov5s-e250-img800.pt --source ../datasets/widerface/images/val/ --folder_pict ../datasets/widerface/wider_face_split/wider_face_val_bbx_gt.txt --conf-thres 0.02 --iou-thres 0.5 --save-txt --save-conf --device 0
...
YOLOv5s summary: 157 layers, 7012822 parameters, 0 gradients, 15.8 GFLOPs
...
Speed: 0.4ms pre-process, 8.6ms inference, 0.8ms NMS per image at shape (1, 3, 640, 640)
Results saved to runs/detect/exp6
0 labels saved to runs/detect/exp6/labels
# cd widerface_evaluate/
# python3 evaluation.py -p ../runs/detect/exp6/labels/ -g ./ground_truth/
Reading Predictions : 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:00<00:00, 235.19it/s]
Processing easy: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:17<00:00,  3.48it/s]
Processing medium: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:17<00:00,  3.49it/s]
Processing hard: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:17<00:00,  3.48it/s]
==================== Results ====================
Easy   Val AP: 0.9513151966498442
Medium Val AP: 0.931779483781727
Hard   Val AP: 0.832029703528219
=================================================
```

## YOLOv5s-face

```shell
# python widerface_detect.py --weights ./runs/train/exp-yolov5sface-e250-img800.pt --source ../datasets/widerface/images/val/ --folder_pict ../datasets/widerface/wider_face_split/wider_face_val_bbx_gt.txt --conf-thres 0.001 --iou-thres 0.6 --save-txt --save-conf --device 0
...
YOLOv5s_face summary: 171 layers, 7038022 parameters, 0 gradients, 15.1 GFLOPs
...
Speed: 0.4ms pre-process, 9.0ms inference, 0.9ms NMS per image at shape (1, 3, 640, 640)
Results saved to runs/detect/exp7
0 labels saved to runs/detect/exp7/labels
# cd widerface_evaluate/
# python3 evaluation.py -p ../runs/detect/exp7/labels/ -g ./ground_truth/
Reading Predictions : 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:00<00:00, 73.54it/s]
Processing easy: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:19<00:00,  3.11it/s]
Processing medium: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:19<00:00,  3.11it/s]
Processing hard: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:19<00:00,  3.13it/s]
==================== Results ====================
Easy   Val AP: 0.9433533134678972
Medium Val AP: 0.9272172318874022
Hard   Val AP: 0.8447000407897594
=================================================
```

```shell
# python widerface_detect.py --weights ./runs/train/exp-yolov5sface-e250-img800.pt --source ../datasets/widerface/images/val/ --folder_pict ../datasets/widerface/wider_face_split/wider_face_val_bbx_gt.txt --conf-thres 0.02 --iou-thres 0.5 --save-txt --save-conf --device 0
...
YOLOv5s_face summary: 171 layers, 7038022 parameters, 0 gradients, 15.1 GFLOPs
...
Speed: 0.4ms pre-process, 9.0ms inference, 0.8ms NMS per image at shape (1, 3, 640, 640)
Results saved to runs/detect/exp8
0 labels saved to runs/detect/exp8/labels
# cd widerface_evaluate/
# python3 evaluation.py -p ../runs/detect/exp8/labels/ -g ./ground_truth/
Reading Predictions : 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:00<00:00, 215.28it/s]
Processing easy: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:18<00:00,  3.36it/s]
Processing medium: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:17<00:00,  3.41it/s]
Processing hard: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 61/61 [00:17<00:00,  3.41it/s]
==================== Results ====================
Easy   Val AP: 0.9422126415903109
Medium Val AP: 0.9247160188989547
Hard   Val AP: 0.8386840917524648
=================================================
```