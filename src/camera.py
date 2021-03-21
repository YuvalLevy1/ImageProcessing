import cv2
from imutils.video import VideoStream


class Camera:
    def __init__(self, port):
        self.port = port
        self.src = VideoStream(src=port + cv2.CAP_DSHOW)
        self.__start()
        self.size = list(self.get_image_bgr().shape)[:2]

    def __start(self):
        self.src.start()

    def get_image_bgr(self):
        return self.src.read()

    def get_image_rgb(self):
        return cv2.cvtColor(self.src.read(), cv2.COLOR_BGR2RGB)

    def get_image_hsv(self):
        return cv2.cvtColor(self.src.read(), cv2.COLOR_BGR2HSV)

    def stop(self):
        self.src.stop()
