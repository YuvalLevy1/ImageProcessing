import cv2
import numpy as np

import camera


def convert_rgb_hsv(rgb):
    return cv2.cvtColor(np.uint8([[rgb]]), cv2.COLOR_RGB2HSV)


def is_collided_with_camera(camera_coordinates, coordinates):
    return camera_coordinates[0] <= coordinates[0] <= camera_coordinates[0] + camera.IMAGE_WIDTH \
           and camera_coordinates[1] <= coordinates[1] <= camera_coordinates[1] + camera.IMAGE_LENGTH
