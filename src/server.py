import imagezmq


class Server:
    def __init__(self):
        self.image_hub = imagezmq.ImageHub()

    def receive_image(self):
        message, image = self.image_hub.recv_image()
        self.image_hub.send_reply(b'OK')
        return message, image
