import imagezmq

import camera


class Client:
    def __init__(self, address, IP_port, camera_port):
        self.sender = imagezmq.ImageSender(connect_to="tcp://{}:{}".format(address, IP_port))
        self.camera = camera.Camera(camera_port)

    def send_image(self):
        self.sender.send_image("frame", self.camera.get_image_bgr())


def main():
    client = Client("127.0.0.1", 5555, 0)
    while True:
        client.send_image()


if __name__ == '__main__':
    main()
