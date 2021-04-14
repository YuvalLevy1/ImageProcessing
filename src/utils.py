import cv2
import numpy as np


def convert_rgb_hsv(rgb):
    return cv2.cvtColor(np.uint8([[rgb]]), cv2.COLOR_BGR2HSV)


def is_collided_with_surface(surface, coordinates):
    return surface.get_rect().collidepoint(coordinates)
