# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 06:35:09 2023

@author: win10
"""

import cv2
import copy
import numpy as np
import tensorflow as tf
from utility import _keypoints_and_edges_for_display
KEYPOINT_EDGE_INDS_TO_COLOR = {
    (0, 1): (255,0,0),
    (0, 2): (255,0,0),
    (1, 3): (255,0,0),
    (2, 4): (255,0,0),
    # (0, 5): (255,0,0),
    # (0, 6): (255,0,0),
    (5, 7): (255,0,0),
    (7, 9): (255,0,0),
    (6, 8): (255,0,0),
    (8, 10):(255,0,0),
    (5, 6): (255,0,0),
    (5, 11):(255,0,0),
    (6, 12):(255,0,0),
    (11, 12):(255,0,0),
    (11, 13): (255,0,0),
    (13, 15): (255,0,0),
    (12, 14): (255,0,0),
    (14, 16): (255,0,0),
}
CONNECTED_PART_NAMES = [
    ("leftHip", "leftShoulder"),
    ("leftElbow", "leftShoulder"),
    ("leftElbow", "leftWrist"),
    ("leftHip", "leftKnee"),
    ("leftKnee", "leftAnkle"),
    ("rightHip", "rightShoulder"),
    ("rightElbow", "rightShoulder"),
    ("rightElbow", "rightWrist"),
    ("rightHip", "rightKnee"),
    ("rightKnee", "rightAnkle"),
    ("leftShoulder", "rightShoulder"),
    ("leftHip", "rightHip"),
]
def draw_prediction_on_image(image, keypoints_with_scores):
    height, width, channel = image.shape
    (keypoint_locs, keypoint_edges,
     edge_colors) = _keypoints_and_edges_for_display(
         keypoints_with_scores, height, width)
    for item in keypoint_locs :
        if item[2]>0.0:
            image = cv2.circle(
                image, (int(item[0]), int(item[1])), 10, (0, 255, 0), -1)
    for line in KEYPOINT_EDGE_INDS_TO_COLOR:

        if keypoints_with_scores[0][0][line[0]][2] > .2 and keypoints_with_scores[0][0][line[1]][2] > 0.2:
            start_point = (int(keypoint_locs[line[0]][
                           0]), int(keypoint_locs[line[0]][1]))
            end_point = (int(keypoint_locs[line[1]][
                         0]), int(keypoint_locs[line[1]][1]))
            color = KEYPOINT_EDGE_INDS_TO_COLOR[line]
            image = cv2.line(image, start_point, end_point, color, 2)
    return image


def wideo(ex_id,frames):
    height = 640
    width = 480
    w =frames[0]['device']['width']*2
    h = frames[0]['device']['height']*2
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter("video.mp4", fourcc, 5.0, (1280,1280))
    # stack=[]
    for frame in frames:
        # stack.append(copy.deepcopy(frame))
        # count1=count(stack,0)
        
        keypoints_with_scores = np.array(
            [[[[frame["frames"][i]["y"]/h, (frame["frames"][i]["x"]/w)+0.3, frame["frames"][i]["score"]]for i in range(17)]]])
    
        frame1 = np.ones((height, width, 3), dtype=np.int32)*255
        display_image = tf.expand_dims(frame1, axis=0)
        display_image = tf.cast(tf.image.resize_with_pad(
            display_image, 1280, 1280), dtype=tf.int32)
        img = draw_prediction_on_image(np.squeeze(
            display_image.numpy(), axis=0), keypoints_with_scores)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(ex_id),
                    (400, 100), font,
                    1, (0, 0, 255),
                    4, cv2.LINE_AA)
        # cv2.putText(img, str(i),
        #             (200, 250), font,
        #             7, (0, 0, 255),
        #             4, cv2.LINE_AA)
        cv2.imshow('frame', cv2.resize(img.astype(np.uint8), (width, height)))
        out.write(img.astype(np.uint8))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # After the loop release the cap object
    # vid.release()
    out.release()
    # Destroy all the windows
    cv2.destroyAllWindows()