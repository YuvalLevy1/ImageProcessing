import cv2
import numpy as np
import pygame

import camera
import filters
import server


class Window:
    def __init__(self, size):
        self.size = size
        self.display = pygame.display.set_mode(self.size, 0)
        pygame.display.set_caption('Image Processor')
        self.clock = pygame.time.Clock()
        self.images = []
        self.filters = []
        self.buttons = []  # button class list

    def __draw_slider(self, slider):
        pygame.draw.rect(self.display, (0, 0, 0), slider.rectangle)
        pygame.draw.circle(self.display, slider.
                           get_circle_color(), (slider.get_circle_coordinates()), slider.get_circle_r())
        self.display.blit(slider.rendered_text, slider.get_text_coordinates())
        font = pygame.font.SysFont('Corbel', 20)
        value = font.render(str(slider.get_value()), True, (0, 0, 0))
        self.display.blit(value, slider.get_value_coordinates())

    def add_button(self, button):
        self.buttons.append(button)

    def __draw_button(self, button):
        pygame.draw.rect(self.display, button.color, button.rectangle)
        self.display.blit(button.rendered_text, button.get_text_coordinates())

    def draw_filter(self, filter):
        for s in filter.sliders:
            self.__draw_slider(s)
        self.display.blit(filter.title, filter.get_title_coordinates())

    def draw_all_buttons(self):
        for button in self.buttons:
            self.__draw_button(button)

    def draw_image(self, image, window_number):
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # transforming the picture from BGR to RGB
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
    print("hello there")


def get_lower_value(value, toleration):
    if value - toleration > 0:
        return value - toleration
    return 0


def get_upper_value(value, toleration):
    if value + toleration < 255:
        return value + toleration
    return 255


def main():
    pygame.init()
    info_object = pygame.display.Info()
    window = Window((info_object.current_w, info_object.current_h))
    hsv_filter = filters.HSV_Filter(300, 520, "HSV filter")
    hsv_filter.add_slider(0, 255, 100, 't')
    hsv_filter.add_slider(0, 255, 100, 'h')
    hsv_filter.add_slider(0, 255, 100, 's')
    hsv_filter.add_slider(0, 255, 100, 'v')
    # button1 = FunctionalButton(200, 200, 100, 50, (100, 100, 100), "fudge", shout)
    # button2 = FunctionalButton(900, 400, 100, 50, (100, 100, 100), "fudge1", shout)
    # button3 = FunctionalButton(400, 600, 100, 50, (100, 100, 100), "fudge2", shout)
    # window.add_button(button1)
    # window.add_button(button2)
    # cam = camera.Camera(0)
    serv = server.Server()
    message, cam = serv.receive_image()
    window.add_camera_window(list(cam.shape)[:2][1])
    window.add_camera_window(list(cam.shape)[:2][1])
    # sliders = [h, s, v, t]

    while True:
        lower_color = np.array([get_lower_value(hsv_filter.get_value("h"), hsv_filter.get_value("t")),
                                get_lower_value(hsv_filter.get_value("s"), hsv_filter.get_value("t")),
                                get_lower_value(hsv_filter.get_value("v"), hsv_filter.get_value("t"))])
        upper_color = np.array([get_upper_value(hsv_filter.get_value("h"), hsv_filter.get_value("t")),
                                get_upper_value(hsv_filter.get_value("s"), hsv_filter.get_value("t")),
                                get_upper_value(hsv_filter.get_value("v"), hsv_filter.get_value("t"))])
        pygame.display.update()
        window.display.fill((255, 255, 255))
        window.clock.tick(60)
        window.draw_filter(hsv_filter)
        window.draw_all_buttons()
        message, image = serv.receive_image()
        window.draw_image(camera.convert_bgr2rgb(image), 0)
        # window.draw_image(camera.convert_bgr2rgb(image), 1)
        mask = cv2.inRange(camera.convert_bgr2hsv(image), lower_color, upper_color)
        # result = cv2.bitwise_and(image, image, mask=mask)
        window.draw_image(camera.convert_bgr2rgb(mask), 1)
        # time.sleep(0.5)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for slider in hsv_filter.sliders:
                    if slider.is_mouse_on_button(pygame.mouse.get_pos()):
                        slider.held = True
            # if button1.is_mouse_on_button(pygame.mouse.get_pos()):
            #     button1.function()
            if event.type == pygame.MOUSEBUTTONUP:
                for slider in hsv_filter.sliders:
                    slider.held = False
        for slider in hsv_filter.sliders:
            slider.move_circle(pygame.mouse.get_pos()[0])
        # print(s.get_value())

        # for button in window.buttons:
        #     if button.is_mouse_on_button(pygame.mouse.get_pos()):
        #         button.function()

    # window.add_button(button3)


if __name__ == '__main__':
    main()
