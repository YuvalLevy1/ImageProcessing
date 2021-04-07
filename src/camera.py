import time

import cv2
from imutils.video import VideoStream

IMAGE_SIZE = 640


def convert_bgr2hsv(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


def convert_bgr2rgb(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def convert_hsv2rgb(image):
    return cv2.cvtColor(image, cv2.COLOR_HSV2RGB)


class Camera:
    def __init__(self, port):
        self.port = port
        self.src = VideoStream(src=port + cv2.CAP_DSHOW)
        self.__start()
        time.sleep(2)

    def __start(self):
        self.src.start()

    def get_image_bgr(self):
        return self.src.read()

    def get_image_size(self):
        return list(self.get_image_bgr().shape)[:2]

    def stop(self):
        self.src.stop()
