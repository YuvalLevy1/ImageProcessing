import math

import pygame

SLIDER_HEIGHT = 5
VALUE_SPACE = 50


class Circle:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color


class Slider:
    def __init__(self, coordinates, min_value, max_value, length, text):
        self.held = False
        self.__x = coordinates[0]
        self.__y = coordinates[1]
        self.__max_x = self.__x + length
        self.min = min_value
        self.max = max_value
        self.__length = length
        self.rectangle = pygame.Rect(self.__x, self.__y, length, SLIDER_HEIGHT)
        self.__circle = Circle(self.__x + int(length / 2), self.__y + 2, SLIDER_HEIGHT, (127, 127, 127))
        font = pygame.font.SysFont('Corbel', 20)
        self.text = text
        self.rendered_text = font.render(text, True, (0, 0, 0))

    """
    moves the circle according to borders
    """

    def move_circle(self, x):
        if not self.held:
            return
        if self.between_borders(x):
            self.__circle.x = x
            return
        self.__circle.x = self.__closest_to(x)

    """
    returns the closest point to x from border 
    """

    def __closest_to(self, x):
        if math.fabs(x - self.__x) > math.fabs(x - self.__max_x):
            return self.__max_x
        return self.__x

    """
    returns true if param x is between the boarders of the slider.
    """

    def between_borders(self, x):
        return self.__max_x >= x >= self.__x

    def get_value(self):
        if self.__circle.x == self.__x:
            return self.min

        if self.__circle.x == self.__max_x:
            return self.max

        return int((self.__circle.x - self.__x) * (self.max / self.__length))

    def get_circle_x_by_value(self, value):
        return (value * self.__length + self.__x * self.max) / self.max

    def is_mouse_on_circle(self, mouse_pos):
        return math.dist(mouse_pos, self.get_circle_coordinates()) <= self.__circle.radius

    def get_circle_coordinates(self):
        return self.__circle.x, self.__circle.y

    def get_size(self):
        return self.rectangle.width + self.rendered_text.get_rect().width + (
                self.__x - self.get_value_coordinates()[0]) + VALUE_SPACE

    def get_circle_r(self):
        return self.__circle.radius

    def get_circle_color(self):
        return self.__circle.color

    def get_text_coordinates(self):
        return self.__max_x + 3, self.__y - 8

    def get_value_coordinates(self):
        return self.__x - VALUE_SPACE, self.__y - 8
