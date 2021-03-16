import pygame

from button import Button


class Window:
    def __init__(self, size):
        self.size = size
        self.display = pygame.display.set_mode(self.size, 0)
        pygame.init()
        pygame.display.set_caption('Image Processor')
        self.images = []
        self.filters = []
        self.buttons = []

    def add_button(self, button):
        self.buttons.append(button)

    def draw_button(self, button):
        pygame.draw.rect(self.display, button.color, button.rectangle)
        self.display.blit(button.text, button.get_text_coordinates())

    def draw_all_buttons(self):
        for button in self.buttons:
            self.draw_button(button)


def shout():
    print("I am pressed")


def main():
    window = Window((1920, 1080))
    button1 = Button(0, 0, 100, 50, (100, 100, 100), "fudge", shout)
    button2 = Button(900, 400, 100, 50, (100, 100, 100), "fudge1", shout)
    button3 = Button(400, 800, 100, 50, (100, 100, 100), "fudge2", shout)
    window.add_button(button1)
    window.add_button(button2)
    window.add_button(button3)

    while True:
        pygame.display.update()
        window.draw_all_buttons()
        for event in pygame.event.get():
            for button in window.buttons:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button.is_mouse_on_button(pygame.mouse.get_pos()):
                        button.function()


if __name__ == '__main__':
    main()
