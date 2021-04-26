import imagezmq

import camera


class Client:
    def __init__(self, address, IP_port, camera_port):
        self.sender = imagezmq.ImageSender(connect_to="tcp://{}:{}".format(address, IP_port))
        self.camera = camera.Camera(camera_port)

    def send_camera_image(self):
        self.send_image("frame", self.camera.get_image_bgr())

    def send_image(self, message, image):
        self.sender.send_image(message, image)


def main():
    client = Client("127.0.0.1", 5555, 1)
    while True:
        client.send_camera_image()


if __name__ == '__main__':
    main()
