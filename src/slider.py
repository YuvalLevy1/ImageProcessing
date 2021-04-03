import math

import pygame

SLIDER_HEIGHT = 5


class Circle:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color


class Slider:
    def __init__(self, x, y, min_value, max_value, length, text):
        self.held = False
        self.__x = x
        self.__y = y
        self.__max_x = x + length
        self.min = min_value
        self.max = max_value
        self.__length = length
        self.rectangle = pygame.Rect(x, y, length, SLIDER_HEIGHT)
        self.__circle = Circle(x + int(length / 2), y + 2, SLIDER_HEIGHT, (127, 127, 127))
        font = pygame.font.SysFont('Corbel', 20)
        self.text = font.render(text, True, (0, 0, 0))

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

    def is_mouse_on_button(self, mouse_pos):
        return math.dist(mouse_pos, self.get_circle_coordinates()) <= self.__circle.radius

    def get_circle_coordinates(self):
        return self.__circle.x, self.__circle.y

    def get_size(self):
        return self.rectangle.width + self.text.get_rect().width + 30

    def get_circle_r(self):
        return self.__circle.radius

    def get_circle_color(self):
        return self.__circle.color

    def get_text_coordinates(self):
        width = self.text.get_rect().width
        return self.__max_x + 3, self.__y - width / 2 - 4

    def get_value_coordinates(self):
        width = self.text.get_rect().width
        return self.__x - 30, self.__y - width / 2 - 4
