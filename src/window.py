import cv2
import pygame

from camera import Camera


class Window:
    def __init__(self, size):
        self.size = size
        self.display = pygame.display.set_mode(self.size, 0)
        pygame.init()
        pygame.display.set_caption('Image Processor')
        self.clock = pygame.time.Clock()
        self.images = []
        self.filters = []
        self.buttons = []  # button class list

    def add_button(self, button):
        self.buttons.append(button)

    def __draw_button(self, button):
        pygame.draw.rect(self.display, button.color, button.rectangle)
        self.display.blit(button.text, button.get_text_coordinates())

    def draw_all_buttons(self):
        for button in self.buttons:
            self.__draw_button(button)

    def draw_image(self, image, window_number):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # transforming the picture from BGR to RGB
        image = pygame.surfarray.make_surface(image)  # making the picture a pygame surface
        image = pygame.transform.rotate(image, -90)
        self.display.blit(image, (self.images[window_number], 0))

    def draw_all_images(self, images):
        for key in images.keys:
            self.draw_image(key, images[key])

    def __calculate_locations(self, amount, width):
        space = int((self.size[0] - width * amount) / (amount + 1))
        print(space)
        coordinate = 0 + space
        locations = [coordinate]
        for i in range(amount - 1):
            locations.append(locations[i] + width + space)
        return locations

    def add_camera_window(self, width):
        self.images = self.__calculate_locations(len(self.images) + 1, width)


def shout():
    print("your mother is a whore")


def main():
    window = Window((1920, 1080))
    # button1 = FunctionalButton(0, 0, 100, 50, (100, 100, 100), "fudge", shout)
    # button2 = FunctionalButton(900, 400, 100, 50, (100, 100, 100), "fudge1", shout)
    # button3 = FunctionalButton(400, 800, 100, 50, (100, 100, 100), "fudge2", shout)
    # window.add_button(button1)
    # window.add_button(button2)
    # window.add_button(button3)
    cam = Camera(0)
    # print(cam.size)
    window.add_camera_window(cam.size[1])
    window.add_camera_window(cam.size[1])
    # window.add_camera_window(cam.size[1])

    while True:
        pygame.display.update()
        window.clock.tick(60)
        # window.draw_all_buttons()
        window.draw_image(cam.get_image_bgr(), 0)
        window.draw_image(cam.get_image_bgr(), 1)
        # window.draw_image(cam.get_image_bgr(), 2)
        # time.sleep(0.5)
        for event in pygame.event.get():
            # for button in window.buttons:
            #     if event.type == pygame.MOUSEBUTTONDOWN:
            #         if button.is_mouse_on_button(pygame.mouse.get_pos()):
            #             button.function()
            pass


if __name__ == '__main__':
    main()
