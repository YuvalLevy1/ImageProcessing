import pygame

import slider


class Filter:
    def __init__(self, x, y, title, sliders):
        self.__x = x
        self.__y = y
        font = pygame.font.SysFont('Corbel', 35)
        self.title = font.render(title, True, (0, 0, 0))
        self.sliders = sliders
        self.width = self.get_width() + 20
        self.height = slider.SLIDER_HEIGHT * len(sliders) * 2 + self.title.get_height() + slider.SLIDER_HEIGHT

    def get_width(self):
        max_width = 0
        for slider in self.sliders:
            if slider.get_size() > max_width:
                max_width = slider.get_size()
        if max_width > self.title.get_width():
            return max_width
        return self.title.get_width()

    def get_title_coordinates(self):
        return (self.__x + self.width) / 2, self.__y

    def get_sliders_coordinates(self):
        coordinates = [(self.__x + 30, self.__y + self.title.get_height() + slider.SLIDER_HEIGHT * 2)]
        for i in range(1, len(self.sliders)):
            coordinates[i] = coordinates[i - 1] + slider.SLIDER_HEIGHT * 2
        return coordinates
