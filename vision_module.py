import cv2
import numpy as np
import pyrealsense2 as rs
import time
import cv2
import time
import openai as openai
from ultralytics import YOLO
import os
import openai
import pyrealsense2 as rs
import numpy as np



def get_xy_depth(depth, x, y):
    # Get the depth frame's dimensions
    width = depth.get_width()
    height = depth.get_height()

    center_x = int(width * x)
    center_y = int(height * y)

    dis_center = round(depth.get_distance(center_x, center_y) * 100, 2)
    return dis_center


def get_center_depth(depth):
    # Get the depth frame's dimensions
    width = depth.get_width()
    height = depth.get_height()

    center_x = int(width / 2)
    center_y = int(height / 2)

    print(width, " ", height)
    dis_center = round(depth.get_distance(center_x, center_y) * 100, 2)
    print("The camera is facing an object ", dis_center, " cm away.")
    return dis_center, (center_x, center_y)

def obj_dec():
    # init rs pipeline
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    # Configure and start the pipeline
    pipeline.start(config)

    detected_pos = []
    detected_objs_names = []
    detected_dis = []
    # action = input("press any key to 'see', press 'q' to quit")
    start = time.time()
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()
    color_image = np.asanyarray(color_frame.get_data())
    depth = frames.get_depth_frame()
    # cv2.imshow('cam', frame)
    vision_model = YOLO('yolov8n.pt')
    results = vision_model(color_image)
    img = results[0].plot()
    cv2.imshow('cam', img)
    cv2.waitKey()
    boxes = results[0].boxes
    # the number of detected objects stored in num_detected_objs, use tensor.
    num_detected_objs = len(boxes.xywhn)
    # define OpenAI message.
    # use detected_pos to store the positions of detected objectives.
    for xywhn in boxes.xywhn:
        x = xywhn[0].item()
        x = round(x, 3)
        detected_pos.append(x)
        y = xywhn[1].item()
        y = round(y, 3)
        detected_pos.append(y)
        obj_depth = get_xy_depth(depth, x, y)
        detected_dis.append(obj_depth)

    # use detected_objs_names to store names of objectives
    name_list = boxes.cls.tolist()

    for name_id in name_list:
        detected_objs_names.append(results[0].names[int(name_id)])

    print(detected_objs_names)
    print(detected_pos)
    print(num_detected_objs)
    print(detected_dis)
    # now we have the variables we need.
    # num_detected_objs is the number of detected objectives,
    # detected_pos are the positions of these detected objectives,
    # detected_objs_names are the names of these detected objectives.
    message = 'number of objectives is ' + (str(num_detected_objs))
    for i in range(num_detected_objs):
        message = message + ' the number ' + str(i+1) + ' objective is ' + str(detected_objs_names[i]) \
                  + ' its x position is ' + str(float(detected_pos[2 * i])) + ' and its y position is ' + \
                  str(float(detected_pos[2 * i + 1])) + ' it is ' + str(
            float(detected_dis[i])) + 'cm away from you. '
    cv2.destroyAllWindows()
    return message
    # pp.say(text)
    # pp.runAndWait()
