import pygame


class Controller:

    name = "Default Controller"
    controller_debug = False

    def __init__(self, handler):
        self.handler = handler
        self.active = True
        self.window = None
        self.handler.add_controller(self)
        self.buttons = set()
        self.active_commands, self.commands, self.inactive_commands = self.create_commands()

    def apply(self, command, *arg):
        if self.active and command in self.active_commands:
            return self.active_commands.get(command)(*arg) or str(command)[0] != "_"
        elif command in self.commands:
            return self.commands.get(command)(*arg) or str(command)[0] != "_"
        elif not self.active and command in self.inactive_commands:
            return self.inactive_commands.get(command)(*arg) or str(command)[0] != "_"
        else:
            if command in self.inactive_commands and self.controller_debug:
                print(f"WARNING: The command ({command}) is in inactive_commands of {self.name}")
            return False

    @classmethod
    def translate(cls, event):
        if event.type == pygame.QUIT:
            return "QUIT"
        elif event.type == pygame.VIDEORESIZE:
            return "RESIZE"
        elif event.type == pygame.MOUSEMOTION:
            return "_MOUSE_MOTION", event.rel
        elif event.type == pygame.KEYDOWN:
            return cls.key_down_translate(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            return cls.mouse_button_up_translate(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            return cls.mouse_button_down_translate(event)

    @staticmethod
    def key_down_translate(event):
        if 97 <= event.key <= 122:
            return event.unicode
        else:
            return event.key

    @staticmethod
    def mouse_button_up_translate(event):
        return {1: "_l_click", 2: "_m_click", 3: "_r_click", 4: "_d_up_click", 5: "_d_down_click"}.get(event.button), event.pos

    @staticmethod
    def mouse_button_down_translate(event):
        return {1: "_l_down", 2: "_m_down", 3: "_r_down", 4: "_d_up_down", 5: "_d_down_down"}.get(event.button), event.pos

    def create_commands(self):
        return {}, {}, {}

    def enable(self):
        self.active = True

    def disable(self):
        self.active = False

    def check_buttons(self, *args):
        for button in self.buttons:
            if button.clicked(*args):
                return True
        return False


class MainController(Controller):

    name = "Main Controller"
    controller_debug = False

    def create_commands(self):
        return ({
                    pygame.K_ESCAPE: self.handler.stop_running,
                },
                {
                    "QUIT": self.handler.stop_running,
                    "RESIZE": self.handler.screen_resize,
                },
                {})
