import pygame

import color


class Button:

    info = {}

    def __init__(self, window, x=0, y=0, label="", height=100, width=250, value=None, func_action=None, func_inaction=None, key=None, clicked=False):
        self.manager = window.manager
        self.window = window
        self.label = label
        self.height = height
        self.width = width-1
        self.value = value
        self.func_action = func_action
        self.func_inaction = func_inaction

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

        if key is not None:
            MultiButton.__init__(self, key, clicked)

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
        text = police.render(str(self.label), 1, color.WHITE)
        self.screen.blit(text, (x + self.width / 2 - text.get_width() / 2,
                                y + self.height / 2 - text.get_height() / 2))

    def collide(self, x, y):
        return 0 <= x - self.x + self.width / 2 - self.window.x <= self.width and 0 <= y - self.y + self.height / 2 - self.window.y <= self.height

    def collide_old(self):
        return self.collide(self.manager.mouse_x, self.manager.mouse_y)

    def is_clicked(self, x, y):
        if self.collide(x, y):
            self.clicked = not self.clicked
            if self.clicked:
                self.color = self.clicked_color
                self.action()
            else:
                self.color = self.unclicked_color
                self.inaction()
            return True
        return False

    def under_mouse(self):
        if not self.clicked and self.collide_old():
            self.color = self.under_mouse_color
        elif not self.clicked:
            self.color = self.unclicked_color

    def inaction(self):
        if self.func_inaction is not None:
            self.func_inaction()

    def action(self):
        if self.func_action is not None:
            self.func_action()
        self.value = not self.value

    def reset(self):
        self.value = True
        self.clicked = False
        self.color = self.unclicked_color


class MultiButton(Button):

    def __init__(self, key, clicked):
        self.key = key
        self.clicked = clicked

        if self.clicked:
            self.info[self.key] = self.value, self
            self.color = self.clicked_color
        elif self.key not in self.info:
            self.info[self.key] = None

    def action(self):
        self.manager.add_debug("i am in action of multi")
        if self.func_action is not None:
            self.func_action()
        if self.info[self.key] is not None:
            self.manager.add_debug("Je check l'ancien")
            self.info.get(self.key)[1].unselect()
            self.info.get(self.key)[1].inaction()
        self.info[self.key] = (self.value, self)

    def inaction(self):
        if self.func_inaction is not None:
            self.func_inaction()
        self.info[self.key] = None

    def unselect(self):
        self.clicked = False
        self.color = self.unclicked_color

    def __repr__(self):
        return str(self.value) + "_" + str(self.key)


class OptionButton(Button):

    def __init__(self, window, x=0, y=0, label="", height=100, width=250, value="", options = ["None"], option_height=None, option_width=None, key=None, clicked=False):
        super().__init__(window, x, y, label, height, width, value, self.main_clicked, self.main_clicked, key, clicked)
        self.options = [Button(self.window, self.x, self.y + self.height / 2 + (i + .5) * (option_height or self.height), option, option_height or height, option_width or width, option, self.option_clicked, self.option_clicked, key=self, clicked=clicked) for i, option in enumerate(options)]
        self.key = key

    def main_clicked(self):
        self.manager.add_debug("Ptn mais tu t'ouvre fdp")
        if self.clicked:
            for option in self.options:
                self.window.new_button(option)
        else:
            for option in self.options:
                self.window.erase_button(option)
        self.clicked = False

    def option_clicked(self):
        for option in self.options:
            self.window.erase_button(option)
        self.clicked = False
        self.color = self.unclicked_color


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
        text = police.render(str(self.options[0].info[self][0]) if self.options[0].info[self] is not None else str(self.label), 1, color.WHITE)
        self.screen.blit(text, (x + self.width / 2 - text.get_width() / 2,
                                y + self.height / 2 - text.get_height() / 2))




