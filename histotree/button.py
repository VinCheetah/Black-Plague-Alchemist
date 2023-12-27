import pygame

import color


class Button:

    def __init__(self, window, x=0, y=0, label="", height=100, width=250, value=0, func_action=None):
        self.manager = window.manager
        self.window = window
        self.label = label
        self.height = height
        self.width = width -1
        self.value = value
        self.func_action = func_action

        self.policy = "monospace"
        self.size = 30
        self.line_color = color.LIGHT_GREY
        self.clicked_color = color.DARK_GREY_1
        self.under_mouse_color = color.DARK_GREY_2
        self.unclicked_color = color.DARK_GREY_3

        self.screen = self.window.window
        self.x, self.y = self.get_coord(x, y)
        self.rect = pygame.Rect(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)
        self.color = self.unclicked_color
        self.clicked = False

    def get_coord(self, x, y):
        if type(x) is str:
            x = {"left": 0 + self.window.border_x + self.width / 2,
                 "right": self.window.width - self.window.border_x - self.width / 2,
                 "center": self.window.width / 2}.get(x)
        if type(y) is str:
            y = {"up": 0 + self.window.border_y + self.height / 2,
                 "down": self.window.height - self.window.border_y - self.height / 2,
                 "center": self.window.height / 2}.get(y)
        return x, y

    def display(self):
        x, y = self.x - self.width / 2, self.y - self.height / 2
        police = pygame.font.SysFont(self.policy, self.size)
        pygame.draw.rect(self.screen, self.color, self.rect)
        pygame.draw.line(self.screen, self.line_color, (x, y), (x + self.width, y))
        pygame.draw.line(self.screen, self.line_color, (x, y), (x, y + self.height))
        pygame.draw.line(self.screen, self.line_color, (x, y + self.height),
                         (x + self.width, y + self.height))
        pygame.draw.line(self.screen, self.line_color, (x + self.width, y),
                         (x + self.width, y + self.height))
        text = police.render(self.label, 1, color.WHITE)
        self.screen.blit(text, (x + self.width / 2 - text.get_width() / 2,
                                y + self.height / 2 - text.get_height() / 2))

    def collide(self, x, y):
        return 0 <= x - self.x + self.width / 2 - self.window.x <= self.width and 0 <= y - self.y + self.height / 2 - self.window.y <= self.height

    def collide_old(self):
        return self.collide(self.manager.mouse_x, self.manager.mouse_y)

    def is_clicked(self, x, y):
        if not self.clicked and self.collide(x, y):
            self.clicked = True
            self.color = self.clicked_color
            self.action()
        else:
            print(f"{x, y} not in {self.x, self.x + self.width} / {self.y, self.y + self.height}")

    def under_mouse(self):
        if not self.clicked and self.collide_old():
            self.color = self.under_mouse_color
        elif not self.clicked:
            self.color = self.unclicked_color

    def action(self):
        if self.func_action is not None:
            self.func_action()


class MultiButton(Button):
    info = {}

    def __init__(self, window, x=0, y=0, label="", height=100, width=250, value=0, key=None, clicked=False):
        super().__init__(window, x, y, label, height, width, value)

        self.key = key
        self.clicked = clicked

        if self.clicked:
            self.info[self.key] = self.value, self
            self.color = self.clicked_color
        else:
            if self.key not in self.info:
                self.info[self.key] = None

    def is_clicked(self, x, y):
        if self.collide(x, y):
            if not self.clicked:
                self.clicked = True
                self.color = self.clicked_color
                self.action()
            else:
                self.clicked = False
                self.color = self.unclicked_color
                self.info[self.key] = None
            return True
        return False

    def action(self):
        if self.info[self.key] is not None:
            self.info.get(self.key)[1].unselect()
        self.info[self.key] = (self.value, self)

    def unselect(self):
        self.clicked = False
        self.color = self.unclicked_color


class SoloButton(Button):

    @classmethod
    def new_button(cls, name, window):
        pass

    def action(self):
        super().action()
        self.value = not self.value

    def reset(self):
        self.value = not self.value
        self.clicked = False
        self.color = self.unclicked_color
