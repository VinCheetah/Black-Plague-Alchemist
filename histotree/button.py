import pygame

import color


class Button:

    def __init__(self, window, x=0, y=0, label="", height=100, width=250, value=None, func_action=None, func_inaction=None, size=None):
        self.manager = window.manager
        self.window = window
        self.label = label
        self.height = height
        self.width = width-1
        self.value = value
        self.func_action = func_action
        self.func_inaction = func_inaction

        self.policy = "monospace"
        self.size = size or 30
        self.line_color = color.LIGHT_GREY
        self.clicked_color = color.DARK_GREY_1
        self.under_mouse_color = color.DARK_GREY_2
        self.unclicked_color = color.DARK_GREY_3

        self.screen = self.window.window
        self.x, self.y = self.get_coord(x, y)
        self.rect = pygame.Rect(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)
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
        self.window.content_height = max(self.window.content_height, self.y + self.height / 2)
        x, y = self.x - self.width / 2 - self.window.view_x, self.y - self.height / 2 - self.window.view_y
        pygame.draw.rect(self.screen, self.color, pygame.Rect(x, y, self.width, self.height))
        pygame.draw.line(self.screen, self.line_color, (x, y), (x + self.width, y))
        pygame.draw.line(self.screen, self.line_color, (x, y), (x, y + self.height))
        pygame.draw.line(self.screen, self.line_color, (x, y + self.height),
                         (x + self.width, y + self.height))
        pygame.draw.line(self.screen, self.line_color, (x + self.width, y),
                         (x + self.width, y + self.height))
        size = self.size
        police = pygame.font.SysFont(self.policy, size)
        text = police.render(str(self.screen_label()), 1, color.WHITE)
        while text.get_width() > self.width:
            size -= 1
            police = pygame.font.SysFont(self.policy, size)
            text = police.render(self.screen_label(), 1, color.WHITE)
        self.screen.blit(text, (x + self.width / 2 - text.get_width() / 2,
                                y + self.height / 2 - text.get_height() / 2))

    def screen_label(self) -> str:
        return self.label

    def collide(self, x, y):
        return 0 <= x - self.x + self.width / 2 - self.window.x + self.window.view_x <= self.width and 0 <= y - self.y + self.height / 2 - self.window.y + self.window.view_y <= self.height

    def collide_mouse(self):
        return self.collide(self.manager.mouse_x, self.manager.mouse_y)

    def is_clicked(self, x, y):
        if self.collide(x, y):
            self.clicked = not self.clicked
            if self.clicked:
                self.action()
            else:
                self.inaction()
            return True
        return False

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

    @property
    def color(self):
        if self.clicked:
            return self.clicked_color
        if self.collide_mouse():
            return self.under_mouse_color
        else:
            return self.unclicked_color

    def __repr__(self):
        return f"Button : {self.label} (clicked : {self.clicked})"


class MultiButton(Button):

    info = {}

    def __init__(self, window, x=0, y=0, label="", height=100, width=250, value=None, func_action=None, func_inaction=None, key="", clicked=False, size=None):
        Button.__init__(self, window, x, y, label, height, width, value, func_action, func_inaction, size)
        self.key = key
        self.clicked = clicked

        if self.clicked:
            self.info[self.key] = self.value, self
        elif self.key not in self.info:
            self.info[self.key] = None

    def apply_click(self):
        self.clicked = True
        if self.info[self.key] is not None:
            self.info.get(self.key)[1].unselect()
            self.info.get(self.key)[1].inaction()
        self.info[self.key] = (self.value, self)

    def action(self):
        self.apply_click()
        if self.func_action is not None:
            self.func_action()

    def inaction(self):
        if self.func_inaction is not None:
            self.func_inaction()
        self.info[self.key] = None

    def unselect(self):
        self.clicked = False

    def __repr__(self):
        return f"MultiButton : {self.label} for key : {self.key} (clicked : {self.clicked})"


class OptionButton(Button):

    def __init__(self, window, x=0, y=0, label="", height=100, width=250, value=None, options=None, option_height=None, option_width=None, option_size=None, option_fun_action=None, option_fun_inaction=None, init_clicked=None):
        Button.__init__(self, window, x, y, label, height, width, value, self.main_clicked, self.main_clicked)
        options = options or ["..."]
        self.option_fun_action = option_fun_action
        self.option_fun_inaction = option_fun_inaction
        self.init_clicked = init_clicked
        self.options = [
            MultiButton(self.window, self.x, self.y + self.height / 2 + (i + .5) * (option_height or self.height),
                        option, option_height or height, option_width or width, option, self.option_clicked,
                        self.option_unclicked, self, False, option_size) for i, option in enumerate(options)]

    def main_clicked(self):
        self.get_options()
        if self.init_clicked is not None:
            for option in self.options:
                if self.init_clicked(option):
                    option.apply_click()

    def main_unclicked(self):
        self.remove_options()

    def option_clicked(self):
        self.remove_options()
        if self.option_fun_action is not None:
            self.option_fun_action()
        self.clicked = True

    def option_unclicked(self):
        self.remove_options()
        if self.option_fun_inaction is not None:
            self.option_fun_inaction()
        self.clicked = False

    def get_options(self):
        for option in self.options:
            self.window.new_button(option)

    def remove_options(self):
        for option in self.options:
            self.window.erase_button(option)

    def screen_label(self) -> str:
        return str(self.options[0].info[self][0]) if self.options[0].info[self] is not None else self.label


class MultiOptionButton(MultiButton):

    def __init__(self, window, x=0, y=0, label="", height=100, width=250, value=None, options=None, option_height=None, option_width=None, key="", clicked=False, option_size=None, option_fun_action=None, option_fun_inaction=None, init_clicked=None, pos="down"):
        MultiButton.__init__(self, window, x, y, label, height, width, value, self.main_clicked, self.main_unclicked, key, False)
        options = options or ["..."]
        match pos:
            case "down":
                dec_x = 0
            case "right":
                dec_x = self.width
            case _:
                dec_x = 0

        self.option_fun_action = option_fun_action
        self.option_fun_inaction = option_fun_inaction
        self.init_clicked = init_clicked
        self.options = [
            MultiButton(self.window, self.x + dec_x, self.y + self.height / 2 + (i + .5) * (option_height or self.height),
                        option, option_height or height, option_width or width, option, self.option_clicked,
                        self.option_unclicked, self, clicked, option_size) for i, option in enumerate(options)]


    def main_clicked(self):
        self.get_options()
        if self.init_clicked is not None:
            for option in self.options:
                if self.init_clicked(option):
                    option.apply_click()

    def main_unclicked(self):
        self.remove_options()

    def option_clicked(self):
        self.remove_options()
        if self.option_fun_action is not None:
            self.option_fun_action()
        self.clicked = True

    def option_unclicked(self):
        self.remove_options()
        if self.option_fun_inaction is not None:
            self.option_fun_inaction()
        self.clicked = False

    def get_options(self):
        for option in self.options:
            self.window.new_button(option)

    def remove_options(self):
        for option in self.options:
            self.window.erase_button(option)

    def screen_label(self) -> str:
        return str(self.options[0].info[self][0]) if self.options[0].info[self] is not None else self.label
