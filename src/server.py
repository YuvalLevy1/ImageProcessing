import socket
import time

import imagezmq


class Server:
    def __init__(self):
        self.image_hub = imagezmq.ImageHub()
        time.sleep(5)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(("127.0.0.1", 1234))

    def receive_image(self):
        message, image = self.image_hub.recv_image()
        self.image_hub.send_reply(b'OK')
        return message, image

    def close_connection(self):
        self.image_hub.close()
        self.socket.send("bye".encode())
