import argparse
import os
import glob
import random
import time
import cv2
import numpy as np
from bin import darknet
from jetcam.csi_camera import CSICamera
# import datetime
detection0 = list()
detection1 = list()

def image_detection(image, network, class_names, class_colors, thresh):
    width = darknet.network_width(network)
    height = darknet.network_height(network)
    darknet_image = darknet.make_image(width, height, 3)

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image_rgb, (width, height),
                               interpolation=cv2.INTER_LINEAR)

    darknet.copy_image_from_bytes(darknet_image, image_resized.tobytes())
    detections = darknet.detect_image(network, class_names, darknet_image, thresh=thresh)
    darknet.free_image(darknet_image)
    # image = darknet.draw_boxes(detections, image_resized, class_colors)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB), detections, image_resized

def detect():
    global detection0, detection1
    config_file = "./yolo-coco/yolov4-tiny.cfg"
    data_file = "./data/coco.data"
    weights = "./yolo-coco/yolov4-tiny.weights"
    batch_size = 1
    thresh = .25
    network, class_names, class_colors = darknet.load_network(
        config_file,
        data_file,
        weights,
        batch_size
    )
    cap0 = CSICamera(capture_device=0, width=224, height=224)
    cap1 = CSICamera(capture_device=1, width=224, height=224)
    while True:
        prev_time = time.time()
        image0 = cap0.read()
        image1 = cap1.read()
        image0, detections0, image_resized0 = image_detection(
            image0, network, class_names, class_colors, thresh
            )
        image1, detections1, image_resized1 = image_detection(
            image1, network, class_names, class_colors, thresh
            )
        # curr_time = datetime.datetime.now()
        detection0.clear()
        detection1.clear()
        for label, confidence, position in detections0:
            detection0.append(label)
        for label, confidence, position in detections1:
            detection1.append(label)
        darknet.print_detections(detections0)
        fps = int(1/(time.time() - prev_time))
        print("FPS: {}".format(fps))
        image0 = darknet.draw_boxes(detections0, image_resized0, class_colors)
        image0 = cv2.cvtColor(image0, cv2.COLOR_BGR2RGB)
        cv2.imshow('camera0', image0)
        image1 = darknet.draw_boxes(detections1, image_resized1, class_colors)
        image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
        cv2.imshow('camera1', image1)
        if cv2.waitKey(1) == 27:
                break


# if __name__ == "__main__":
#     # unconmment next line for an example of batch processing
#     # batch_detection_example()
#     detect()
