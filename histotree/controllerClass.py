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

    def enable(self, *args):
        self.active = True
        self.add_enable(*args)

    def add_enable(self, *args):
        pass

    def disable(self):
        self.active = False
        self.add_disable()

    def add_disable(self):
        pass

    def check_buttons(self, *args):
        for button in self.buttons.copy():
            if button.is_clicked(*args):
                return True
        return False

    def clicked_node(self, p, extension=1.):
        sel_node, dist = None, inf
        for node in self.manager.histo_tree.nodes:
            d_node = self.manager.dist(p, node.pos)
            if dist > d_node <= extension * node.size:
                sel_node, dist = node, d_node
        return sel_node

    def clicked_link(self, p, extension=1.):
        sel_link, dist = None, inf
        for link in self.manager.histo_tree.links:
            d_link = self.manager.dist_seg_point(link.n1.pos, link.n2.pos, p)
            if dist > d_link <= extension * link.size:
                sel_link, dist = link, d_link
        return sel_link






class MainController(Controller):
    name = "Main Controller"
    controller_debug = False

    def create_commands(self):
        return (
            {
                pygame.K_ESCAPE: self.manager.start_menu,

                "m": self.manager.start_menu,

                "n": self.manager.insert_text_controller.enable,

                "s": self.manager.favorite_save,
                "p": self.manager.print_histo_tree,
                "f": self.flip_tool,
                "t": self.hide_tool,

                "q": self.show_controllers
            },
            {
                "QUIT": self.manager.stop_running,
                "RESIZE": self.manager.screen_resize,
            },
            {},
        )

    def show_controllers(self):
        self.manager.add_debug("\n".join(controller.name for controller in self.manager.controllers if controller.active))

    def flip_tool(self):
        if not self.manager.hidden_tools:
            self.manager.main_window.x = self.manager.tool_size - self.manager.main_window.x
            self.manager.tool_window.x = (self.manager.width - self.manager.tool_size) - self.manager.tool_window.x
            self.manager.debug_window.x = (self.manager.width - self.manager.tool_size + 10) - self.manager.debug_window.x

    def hide_tool(self):
        if not self.manager.hidden_tools:
            self.manager.main_window.x = 0
            self.manager.main_window.set_dim(new_width=self.manager.width)
            self.manager.tool_window.retire_windows()
        else:
            self.manager.main_window.set_dim(new_width=self.manager.width - self.manager.tool_size)
            self.manager.main_window.x = (self.manager.tool_window.x == 0) * self.manager.tool_size
            self.manager.tool_window.add_windows()
        self.manager.hidden_tools = not self.manager.hidden_tools


class MapController(Controller):

    name = "Map Controller"
    controller_debug = False

    def create_commands(self):
        return (
            {
                "_d_up_click": self.zoom,
                "_d_down_click": self.un_zoom,
                "_l_click": self.left_click,
                "_r_click": self.right_click,

                "_MOUSE_MOTION": self.manager.move_map,

                "h": self.manager.view_home,
            },
            {},
            {}
        )

    def un_zoom(self, *args):
        if not self.manager.main_window.collide_mouse():
            return False
        self.manager.unzoom_move()

    def zoom(self, *args):
        if not self.manager.main_window.collide_mouse():
            return False
        self.manager.zoom_move()

    def left_click(self, *args):
        if not self.manager.main_window.collide_mouse():
            return False
        if self.check_buttons(*args):
            return True
        p = self.manager.un_view(args)
        if not self.manager.moving_map:
            node = self.clicked_node(p, 1.5)
            if node is not None:
                self.manager.select(node)
                self.manager.view_move(*node.pos)
                return True
            link = self.clicked_link(p, 2)
            if link is not None:
                self.manager.select(link)
                self.manager.view_move(*link.middle)
                return True
            if self.manager.selected is None:
                self.manager.histo_tree.add_node(*p)
            else:
                self.manager.unselect()
        else:
            self.manager.buildable = True
            self.manager.moving_map = False
        return True

    def right_click(self, *args):
        if not self.manager.main_window.collide_mouse():
            return False
        if self.check_buttons(*args):
            return True
        if not self.manager.moving_map:
            if self.manager.selected is None:
                self.manager.add_debug("right")
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

                "q": self.show_controllers,

                pygame.K_RETURN: self.enter,
                pygame.K_ESCAPE: self.manager.stop_running,
            },
            {},
            {
            }
        )


    def show_controllers(self):
        self.manager.add_debug("\n".join(controller.name for controller in self.manager.controllers if controller.active))
        print("\n".join(controller.name for controller in self.manager.controllers if controller.active))

    def enter(self):
        return self.manager.menu_window.start_button.action()

    def left_click(self, *args):
        return self.check_buttons(*args)

        
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
            {},
            {}
        )


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

class LinkController(Controller):
    name = "Link Controller"

    def add_init(self) -> None:
        self.move_link = False

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
        if self.move_link or (self.manager.selected.dist(*self.manager.un_view(self.manager.mouse_pos)) < self.manager.selected.size and pygame.mouse.get_pressed()[0]):
            self.move_link = True
            if not pygame.mouse.get_pressed()[0]:
                self.move_link = False
            else:
                self.manager.selected.move_pos(args[0] / self.manager.zoom, args[1] / self.manager.zoom)
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

                "_d_up_click": self.manager.tool_window_view_up,
                "_d_down_click": self.manager.tool_window_view_down,

                pygame.K_DOWN: self.manager.tool_window_view_down,
                pygame.K_UP: self.manager.tool_window_view_up,
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
                link = self.clicked_link(p, 1.5)
                if link is not None:
                    self.manager.histo_tree.delete_link(link)
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



class DebugController(Controller):
    name = "Debug Controller"
    controller_debug = False

    def create_commands(self):
        return (
            {
                "_l_click": self.left_click,

                "_d_up_click": self.manager.debug_window_view_up,
                "_d_down_click": self.manager.debug_window_view_down,

                "c": self.clear_text,

                pygame.K_DOWN: self.manager.debug_window_view_down,
                pygame.K_UP: self.manager.debug_window_view_up,
            },
            {},
            {}
        )

    def clear_text(self):
        self.manager.debug_window.clear_text()

    def left_click(self, *args):
        return self.manager.debug_window.set_down()


class PropertiesController(Controller):
    name = "Properties Controller"
    controller_debug = False

    def new_init(self, obj):
        self.object = obj
        self.enable()


    def create_commands(self):
        return (
            {
                "_l_click": self.left_click,

                #"_d_up_click": self.manager.debug_window_view_up,
                #"_d_down_click": self.manager.debug_window_view_down,

                #pygame.K_DOWN: self.manager.debug_window_view_down,
                #pygame.K_UP: self.manager.debug_window_view_up,
            },
            {},
            {}
        )

    def left_click(self, *args):
        return self.check_buttons(*args)



class InsertTextController(Controller):

    name = "Insert Text Controller"

    def add_init(self):
        self.button = None

    def add_enable(self, active_button):
        self.stop_connection()
        self.button = active_button

    def create_commands(self):
        return ({chr(i): (lambda c=i: self.char_clicked(chr(c))) for i in range(220)} |
                {pygame.K_BACKSPACE: self.delete_last,
                 pygame.K_RETURN: self.stop_connection},
                {},
                {})

    def stop_connection(self):
        if self.button is not None:
            self.button.clicked = False
            self.button.inaction()
            self.button = None

    def char_clicked(self, char):
        self.button.value += char

    def delete_last(self):
        if len(self.button.value) > 0:
            self.button.value = self.button.value[:-1]
