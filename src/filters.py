import numpy as np
import pygame

import slider


class Filter:
    def __init__(self, x, y, title):
        self.__x = x
        self.__y = y
        font = pygame.font.SysFont('Corbel', 30)
        self.title = font.render(title, True, (0, 0, 0))
        self.width = self.title.get_width()
        self.height = self.title.get_height()
        self.sliders = []
        self.sliders_coordinates = [(self.__x + slider.VALUE_SPACE,
                                     self.__y + self.title.get_height() + slider.SLIDER_HEIGHT * 2)]
        self.slider_amount = 0

    def get_width(self):
        max_width = 0
        for slider in self.sliders:
            if slider.get_size() > max_width:
                max_width = slider.get_size()
        if max_width > self.title.get_width():
            return max_width
        return self.title.get_width()

    def get_height(self):
        return slider.SLIDER_HEIGHT * len(self.sliders) * 2 + self.title.get_height() + slider.SLIDER_HEIGHT

    def get_title_coordinates(self):
        return self.__x + self.width / 2 - self.title.get_width() / 2 - 15, self.__y

    def __get_slider_coordinates(self):
        self.sliders_coordinates.append(
            (self.sliders_coordinates[-1][0], self.sliders_coordinates[-1][1] + slider.SLIDER_HEIGHT * 5))
        return self.sliders_coordinates[-1]

    def add_slider(self, min_value, max_value, length, text):
        if self.slider_amount == 0:
            s = slider.Slider(self.sliders_coordinates[0],
                              min_value, max_value, length, text)
        else:
            s = slider.Slider(self.__get_slider_coordinates(), min_value, max_value, length, text)
        self.sliders.append(s)
        self.width = self.get_width()
        self.slider_amount += 1


class HSV_Filter(Filter):
    def __init__(self, x, y, title):
        super().__init__(x, y, title)
        self.add_slider(0, 255, 100, 't')
        self.add_slider(0, 255, 100, 'h')
        self.add_slider(0, 255, 100, 's')
        self.add_slider(0, 255, 100, 'v')

    def get_value(self, text):
        for slider in self.sliders:
            if slider.text == text:
                return slider.get_value()

    def get_lower_color(self):
        return np.array([get_lower_value(self.get_value("h"), self.get_value("t")),
                         get_lower_value(self.get_value("s"), self.get_value("t")),
                         get_lower_value(self.get_value("v"), self.get_value("t"))])

    def get_upper_color(self):
        return np.array([get_upper_value(self.get_value("h"), self.get_value("t")),
                         get_upper_value(self.get_value("s"), self.get_value("t")),
                         get_upper_value(self.get_value("v"), self.get_value("t"))])


def get_lower_value(value, toleration):
    if value - toleration > 0:
        return value - toleration
    return 0


def get_upper_value(value, toleration):
    if value + toleration < 255:
        return value + toleration
    return 255
