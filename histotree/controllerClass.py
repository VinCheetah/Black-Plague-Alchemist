import pygame
import button
from math import inf


class Controller:
    name = "Default Controller"
    controller_debug = False

    def __init__(self, manager):
        from manager import HistoTreeManager
        self.manager: HistoTreeManager = manager
        self.active: bool = False
        self.window = None
        self.manager.add_controller(self)
        self.buttons = set()
        self.active_commands, self.commands, self.inactive_commands = self.create_commands()

        self.add_init()

    def add_init(self) -> None:
        pass

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
        self.add_enable()

    def add_enable(self):
        pass

    def disable(self):
        self.active = False
        self.add_disable()

    def add_disable(self):
        pass

    def check_buttons(self, *args):
        for button in self.buttons:
            if button.is_clicked(*args):
                return True
        return False

    def check_under_mouse(self, *args):
        for button in self.buttons:
            button.under_mouse()

    def clicked_node(self, p, extension=1.):
        sel_node, dist = None, inf
        for node in self.manager.histo_tree.nodes:
            d_node = self.manager.dist(p, node.pos)
            if dist > d_node <= extension * node.size:
                sel_node, dist = node, d_node
        return sel_node






class MainController(Controller):
    name = "Main Controller"
    controller_debug = False

    def create_commands(self):
        return (
            {
                pygame.K_ESCAPE: self.manager.stop_running,

                "m": self.manager.start_menu,
                "s": self.manager.favorite_save,
                "p": self.manager.print_histo_tree
            },
            {
                "QUIT": self.manager.stop_running,
                "RESIZE": self.manager.screen_resize,
            },
            {},
        )


        
        
class MapController(Controller):

    name = "Map Controller"
    controller_debug = False

    def create_commands(self):
        return (
            {
                "_d_up_click": self.manager.zoom_move,
                "_d_down_click": self.manager.unzoom_move,
                "_l_click": self.left_click,
                "_r_click": self.right_click,

                "_MOUSE_MOTION": self.manager.move_map,

                "h": self.manager.view_home,
            },
            {},
            {}
        )

    def left_click(self, *args):
        if self.check_buttons(*args):
            return True
        if not self.manager.moving_map:
            if self.manager.selected is None:
                self.manager.histo_tree.add_node(*self.manager.un_view(args))
            else:
                self.manager.unselect()
        else:
            self.manager.buildable = True
            self.manager.moving_map = False
        return True

    def right_click(self, *args):
        if self.check_buttons(*args):
            return True
        if not self.manager.moving_map:
            if self.manager.selected is None:
                print("right")
            else:
                self.manager.unselect()
        else:
            self.manager.buildable = True
            self.manager.moving_map = False
        return True



class MenuController(Controller):
    name = "Menu Controller"

    def create_commands(self):
        return (
            {
                "_l_click": self.left_click,
                "_MOUSE_MOTION": self.mouse_motion,

                pygame.K_RETURN: self.enter,
            },
            {},
            {
            }
        )

    def enter(self):
        print("Yoow")
        self.manager.menu_window.start_button.action()

    def left_click(self, *args):
        return self.check_buttons(*args)

    def mouse_motion(self, *args):
        self.check_under_mouse(*args)
        
        
class SelectionController(Controller):

    name = "Selection Controller"

    def __init__(self, game):
        super().__init__(game)
        self.disable()

    def create_commands(self):
        return (
            {
                pygame.K_BACKSPACE: self.manager.delete_selected,
                "i": self.print_infos
            },
            {
                "_l_click": self.find_selected
            },
            {}
        )

    def find_selected(self, x, y):
        p = self.manager.un_view((x, y))
        if not self.manager.moving_map:
            node = self.clicked_node(p, 1.5)
            if node is not None:
                self.manager.select(node)
                self.manager.view_move(*node.pos)
                self.enable()
                self.manager.node_controller.enable()
                return True
        return False

    def print_infos(self):
        self.manager.add_debug(self.manager.selected)


class NodeController(Controller):

    def add_init(self) -> None:
        self.move_node = False

    name = "Node Controller"
    def create_commands(self):
        return (
            {
                #"_l_click":None,
                "_MOUSE_MOTION": self.mouse_motion,

                "r": self.root_selected,
            },
            {},
            {}
        )

    def mouse_motion(self, *args):
        if self.move_node or (self.manager.selected.dist(*self.manager.un_view(self.manager.mouse_pos)) < self.manager.selected.size and pygame.mouse.get_pressed()[0]):
            self.move_node = True
            if not pygame.mouse.get_pressed()[0]:
                self.move_node = False
            else:
                self.manager.selected.set_pos(self.manager.un_view(self.manager.mouse_pos))
            return True
        return False

    def root_selected(self):
        self.manager.histo_tree.set_root(self.manager.selected)


class ToolController(Controller):
    name = "Tool Controller"
    controller_debug = False

    def add_init(self) -> None:
        self.aux = None

    def create_commands(self):
        return (
            {
                "_l_click": self.left_click,
                "_MOUSE_MOTION": self.mouse_motion,
            },
            {},
            {}
        )

    def left_click(self, *args):
        p = self.manager.un_view(args)
        if self.check_buttons(*args):
            return True
        if button.MultiButton.info["node_tool"] is not None:
            if button.MultiButton.info["node_tool"][0] == "link":
                node = self.clicked_node(p)
                if node is not None:
                    return self.manager.histo_tree.add_link(self.manager.selected, node)
            elif button.MultiButton.info["node_tool"][0] == "birth":
                node = self.clicked_node(p)
                if node is None:
                    self.manager.histo_tree.add_link(self.manager.selected, self.manager.histo_tree.add_node(*p))
                    return True
        if button.MultiButton.info["main_tool"] is not None:
            if button.MultiButton.info["main_tool"][0] == "delete":
                node = self.clicked_node(p, 1.5)
                if node is not None:
                    self.manager.histo_tree.delete_node(node)
                    return True
            if button.MultiButton.info["main_tool"][0] == "link":
                node = self.clicked_node(p, 1.5)
                if node is not None:
                    if self.aux is not None:
                        if self.aux != node:
                            self.manager.histo_tree.add_link(self.aux, node)
                        self.aux = None
                    else:
                        self.aux = node
                    return True

    def mouse_motion(self, *args):
        self.check_under_mouse(*args)


class DebugController(Controller):
    name = "Debug Controller"
    controller_debug = False

    def create_commands(self):
        return (
            {
                "_l_click": self.left_click,

                "_d_up_click": self.manager.debug_window_view_up,
                "_d_down_click": self.manager.debug_window_view_down,

                pygame.K_DOWN: self.manager.debug_window_view_down,
                pygame.K_UP: self.manager.debug_window_view_up,
            },
            {},
            {}
        )

    def left_click(self, *args):
        return self.manager.debug_window.set_down()
