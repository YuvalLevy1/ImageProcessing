import sys
import threading
import time

import cv2
import pygame

import camera
import filters
import server
from buttons import BaseButton
from utils import convert_rgb_hsv, is_collided_with_camera

image = None  # the image displayed on screen.
mask = None  # the image after color filtration.
distance = 0  # the distance of the contour from the camera.
contours = []  # the contours found by open-cv, can contain background noises.
running = True  # the variable responsible for stopping the program. when false the program will stop.
serv = server.Server()  # the server is responsible for receiving the images and closing the program.

"""
the function is responsible for updating the global variable "image" according to the photos sent 
from the client.
"""


def get_image():
    global image, running, serv
    while running:
        message, image = serv.receive_image()
    print("stopped receiving")


"""
the function receives the area filter and a contour and checks
if the contour's area is between the parameters the user set.
"""


def is_according_to_filter(filter, contour):
    max_area = filter.get_value("max area")
    min_area = filter.get_value("min area")
    area = find_contour_area(contour)
    if filter.get_max_value("max area") == max_area:
        if min_area == 0:
            return True
        return area >= min_area

    if min_area == 0:
        return max_area >= area

    if filter.get_value("max area") >= find_contour_area(contour) >= filter.get_value("min area"):
        return True

    return False


"""
the function is responsible for handling the contours.
it runs in a separated thread and calls the function 
that are responsible for finding the contours, then find the one matching the filter and eventually
calculate its distance to the camera.
"""


def calculate_contours(window, contour_filter, toggle_contours):
    global contours, distance, running
    while running:
        find_contours(toggle_contours)
        if contours is not None and len(contours) > 0:
            for index in range(len(contours)):
                if find_contour_area(contours[index]) < 100:
                    continue
                if is_according_to_filter(contour_filter, contours[index]):
                    moment = cv2.moments(contours[index])
                    coordinates = find_contour_coordinates(window.image_locations[1], moment)
                    if coordinates is not None:
                        window.contour_centroid = coordinates
                        distance = get_distance_to_camera(contours[index], 34)
    print("stopped calculating contours\n")


"""
returns the distance to the camera according to the contour's width
"""


def get_distance_to_camera(contour, real_width):
    return real_width * 1250.97996 / find_contour_width(contour) / 2


"""
the function is responsible for finding contours.
the params in cv2.findContours define the array returned.
RETR_EXTERNAL defines the hierarchy so only external points will be returned, thus saving memory.
CHAIN_APPROX_SIMPLE sets the function to only return the necessary point for the contour. for example, if 
the contour is shaped as a rectangle, only 4 points will be returned.
"""


def find_contours(toggle_button):
    global contours, mask, distance
    if mask is not None and toggle_button.is_pressed():
        contours, h = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        distance = 0


"""
calculating the center of a contour in a certain moment.
the calculation for a contour's center is relative to the image and therefore
needs to be subtracted from the coordinates of the end of the mask.
"""


def find_contour_coordinates(mask_coordinates, moment):
    try:
        return (mask_coordinates + camera.IMAGE_WIDTH - int(moment['m10'] / moment['m00']),
                int(moment['m01'] / moment['m00']))
    except ZeroDivisionError:
        return None


def find_contour_area(contour):
    return cv2.contourArea(contour)


def find_contour_width(contour):
    return cv2.boundingRect(contour)[2]


class Window:
    def __init__(self, size):
        self.contour_centroid = None
        self.size = size
        self.display = pygame.display.set_mode(self.size, 0)
        pygame.display.set_caption('Image Processor')
        self.clock = pygame.time.Clock()
        self.image_locations = []
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

    def add_button(self, button):
        self.buttons.append(button)

    def add_camera_window(self, width):
        self.image_locations = self.__calculate_image_locations(len(self.image_locations) + 1, width)

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

    def __calculate_image_locations(self, amount, width):
        space = int((self.size[0] - width * amount) / (amount + 1))
        coordinate = 0 + space
        locations = [coordinate]
        for i in range(amount - 1):
            locations.append(locations[i] + width + space)
        return locations

    def get_sliders(self):
        sliders = []
        for f in self.filters:
            sliders += f.sliders
        return sliders

    def get_image_color(self, coordinates):
        print("rgb is:{}".format(self.display.get_at(coordinates)))
        hsv = convert_rgb_hsv(self.display.get_at(coordinates))
        print("hsv is:{}".format(hsv[0][0]))
        return hsv[0][0]

    def get_filter(self, title):
        for filter in self.filters:
            if filter.title == title:
                return filter


def main():
    global image, mask, contours, distance, running

    receiving = threading.Thread(target=get_image)
    receiving.start()

    while image is None:
        time.sleep(5)

    pygame.init()
    font = pygame.font.SysFont('Corbel', 20)
    window = Window((1280, 650))
    window.add_camera_window(camera.IMAGE_WIDTH)
    window.add_camera_window(camera.IMAGE_WIDTH)

    hsv_filter = filters.HSV_Filter(30, 510)
    window.add_filter(hsv_filter)
    contour_filter = filters.ContourFilter(200, 510)
    window.add_filter(contour_filter)

    toggle_contours = BaseButton(1000, 550, 160, 50, (100, 100, 100), "toggle contours")
    window.add_button(toggle_contours)

    contours_thread = threading.Thread(target=calculate_contours, args=[window, contour_filter, toggle_contours])
    contours_thread.start()

    while True:
        lower_color = hsv_filter.get_lower_color()
        upper_color = hsv_filter.get_upper_color()

        pygame.display.update()
        window.display.fill((255, 255, 255))
        window.clock.tick(30)

        window.draw_all_filters()
        window.draw_all_buttons()

        mask = cv2.inRange(camera.convert_bgr2hsv(image), lower_color, upper_color)
        window.draw_all_images([camera.convert_bgr2rgb(image), camera.convert_bgr2rgb(mask)])

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                print("exiting game")
                running = False
                pygame.display.quit()
                pygame.quit()
                serv.close_connection()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for slider in window.get_sliders():
                    if slider.is_mouse_on_circle(pygame.mouse.get_pos()):
                        slider.held = True

                if is_collided_with_camera((window.image_locations[0], 0), pygame.mouse.get_pos()):
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

        if window.contour_centroid is not None and toggle_contours.is_pressed():
            pygame.draw.circle(window.display, (70, 150, 70),
                               window.contour_centroid,
                               5)
            window.contour_centroid = None

        rendered_distance = font.render(str(distance), True, (0, 0, 0))
        window.display.blit(rendered_distance, (1200, 565))


if __name__ == '__main__':
    main()
