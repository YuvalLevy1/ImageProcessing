import pygame


class Button:
    def __init__(self, x, y, width, height, color, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rectangle = pygame.Rect(x, y, width, height)
        self.color = color
        font = pygame.font.SysFont('Corbel', 35)
        self.text = font.render(text, True, (255, 255, 255))

    def is_mouse_on_button(self, mouse_pos):
        if self.rectangle.collidepoint(mouse_pos):
            return True

    def get_text_coordinates(self):
        rect = self.text.get_rect()
        width = rect.width
        height = rect.height
        return self.x + (self.width - width) / 2, self.y + (self.height - height) / 2
