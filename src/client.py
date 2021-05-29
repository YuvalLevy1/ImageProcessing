import socket
import threading

import imagezmq

import camera


def listen_to_server(s, client):
    while True:
        data = s.recv(1024).decode()
        print("got a message: {}".format(data))
        if data == "bye":
            break
    client.socket.close()
    client.sender.close()


class Client:
    def __init__(self, address, IP_port, camera_port):
        self.sender = imagezmq.ImageSender(connect_to="tcp://{}:{}".format(address, IP_port))
        self.camera = camera.Camera(camera_port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("127.0.0.1", 1234))

    def send_camera_image(self):
        self.send_image("frame", self.camera.get_image_bgr())

    def send_image(self, message, image):
        self.sender.send_image(message, image)


def main():
    client = Client("127.0.0.1", 5555, 0)
    client.socket.listen()
    server, server_addr = client.socket.accept()
    listening = threading.Thread(target=listen_to_server, args=[server, client])
    listening.start()
    try:
        while True:
            client.send_camera_image()
    except imagezmq.zmq.error.ContextTerminated:
        print("done")


if __name__ == '__main__':
    main()
