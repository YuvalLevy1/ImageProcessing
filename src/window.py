import threading
import time

import cv2
import pygame

import buttons as button
import camera
import filters
import server
from utils import convert_rgb_hsv, is_collided_with_surface

image = None
mask = None
contours = None


def get_image():
    global image
    serv = server.Server()
    while True:
        message, image = serv.receive_image()


def event_handler(window):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for slider in window.get_sliders():
                    if slider.is_mouse_on_circle(pygame.mouse.get_pos()):
                        slider.held = True

                if is_collided_with_surface(window.current_image, pygame.mouse.get_pos()):
                    window.get_filter("hsv"). \
                        change_hsv_values(window.get_image_color(pygame.mouse.get_pos()))

                for button in window.buttons:
                    if button.is_mouse_on_button(pygame.mouse.get_pos()):
                        button.toggle = not button.toggle
                        print("toggling button")

            if event.type == pygame.MOUSEBUTTONUP:
                for slider in window.get_sliders():
                    slider.held = False

        for slider in window.get_sliders():
            slider.move_circle(pygame.mouse.get_pos()[0])


def find_contours(toggle_button):
    global contours, mask
    if toggle_button.is_pressed() and mask is not None:
        contours, h = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours is not None:
        print(contours)


class Window:
    def __init__(self, size):
        self.size = size
        self.display = pygame.display.set_mode(self.size, 0)
        pygame.display.set_caption('Image Processor')
        self.clock = pygame.time.Clock()
        self.image_locations = []
        self.current_image = None
        self.filters = []
        self.buttons = []

    def __draw_slider(self, slider):
        pygame.draw.rect(self.display, (0, 0, 0), slider.rectangle)
        pygame.draw.circle(self.display, slider.
                           get_circle_color(), (slider.get_circle_coordinates()), slider.get_circle_r())
        self.display.blit(slider.rendered_text, slider.get_text_coordinates())
        font = pygame.font.SysFont('Corbel', 20)
        value = font.render(str(slider.get_value()), True, (0, 0, 0))
        self.display.blit(value, slider.get_value_coordinates())

    def __draw_button(self, button):
        pygame.draw.rect(self.display, button.color, button.rectangle)
        self.display.blit(button.text, button.get_text_coordinates())

    def __draw_filter(self, filter):
        for s in filter.sliders:
            self.__draw_slider(s)
        self.display.blit(filter.title_font, filter.get_title_coordinates())

    def __draw_image(self, image, window_number):
        image = pygame.surfarray.make_surface(image)  # making the picture a pygame surface
        image = pygame.transform.rotate(image, -90)
        self.display.blit(image, (self.image_locations[window_number], 0))

    def update_current_image(self, image):
        image = pygame.surfarray.make_surface(image)  # making the picture a pygame surface
        image = pygame.transform.rotate(image, -90)
        self.current_image = image

    def add_button(self, button):
        self.buttons.append(button)

    def add_camera_window(self, width):
        self.image_locations = self.__calculate_locations(len(self.image_locations) + 1, width)

    def add_filter(self, filter):
        self.filters.append(filter)

    def draw_all_buttons(self):
        for button in self.buttons:
            self.__draw_button(button)

    def draw_all_images(self, images):
        count = 0
        for image in images:
            self.__draw_image(image, count)
            count += 1

    def draw_all_filters(self):
        for filter in self.filters:
            self.__draw_filter(filter)

    def __calculate_locations(self, amount, width):
        space = int((self.size[0] - width * amount) / (amount + 1))
        coordinate = 0 + space
        locations = [coordinate]
        for i in range(amount - 1):
            locations.append(locations[i] + width + space)
        return locations

    def get_sliders(self):
        sliders = []
        for f in self.filters:
            sliders.append(f.sliders)
        return sliders[0]

    def get_image_color(self, coordinates):
        if self.current_image is not None:
            print("rgb is:{}".format(self.current_image.get_at(coordinates)))
            hsv = convert_rgb_hsv(self.current_image.get_at(coordinates))
            print("hsv is:{}".format(hsv[0][0]))
            return hsv[0][0]

    def get_filter(self, title):
        for filter in self.filters:
            if filter.title == title:
                return filter


def main():
    global image, mask
    pygame.init()
    info_object = pygame.display.Info()
    window = Window((info_object.current_w, info_object.current_h))

    hsv_filter = filters.HSV_Filter(300, 520)
    window.add_filter(hsv_filter)

    toggle_contours = button.BaseButton(600, 500, 160, 50, (100, 100, 100), "toggle contours")
    window.add_button(toggle_contours)

    receiving = threading.Thread(target=get_image)
    events = threading.Thread(target=event_handler, args=[window])
    # contours_thread = threading.Thread(target=find_contours, args=[toggle_contours])

    receiving.start()
    events.start()
    # contours_thread.start()

    while image is None:
        time.sleep(5)

    window.add_camera_window(camera.IMAGE_SIZE)
    window.add_camera_window(camera.IMAGE_SIZE)

    while True:
        lower_color = hsv_filter.get_lower_color()
        upper_color = hsv_filter.get_upper_color()

        pygame.display.update()
        window.display.fill((255, 255, 255))
        window.clock.tick(60)

        window.draw_all_filters()
        window.draw_all_buttons()

        mask = cv2.inRange(camera.convert_bgr2hsv(image), lower_color, upper_color)
        window.draw_all_images([camera.convert_bgr2rgb(image), camera.convert_bgr2rgb(mask)])
        window.update_current_image(image)
        find_contours(toggle_contours)
        if len(pygame.event.get(eventtype=pygame.QUIT)) != 0:
            break


if __name__ == '__main__':
    main()
