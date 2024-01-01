import pygame
import color
import boundedValue
from button import Button, OptionButton, MultiButton, MultiOptionButton
import math


class Window:

    def __init__(self, manager, controller, x=0, y=0, name="Window", width=800, height=800, alpha=255, moveable=True, selectionable=True, closable=True):
        self.manager = manager

        self.controller = controller

        self.x = x
        self.y = y

        self.view_x = boundedValue.BoundedValue(0, 0, 0)
        self.view_y = boundedValue.BoundedValue(0, 0, 0)

        self.content_height = 0

        self.font = pygame.font.SysFont("Courier New", 20)
        self.width = width
        self.height = height
        self.alpha = alpha
        self.background_color = color.BLACK
        self.writing_color = color.WHITE
        self.name = name
        self.border_x = 5
        self.border_y = 5
        self.moveable = moveable
        self.selectionable = selectionable
        self.closable = closable

        self.buttons = set()

        self.window = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.active = True
        self.content = None

        self.additionnal_init()

    def additionnal_init(self):
        pass

    def collide(self, x, y):
        return 0 <= x - self.x <= self.width and 0 <= y - self.y <= self.height

    def collide_mouse(self):
        return 0 <= self.manager.mouse_x - self.x <= self.width and 0 <= self.manager.mouse_y - self.y <= self.height

    def set_dim(self, new_height=None, new_width=None):
        self.width = new_width or self.width
        self.height = new_height or self.height
        self.window = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

    def window_view_down(self):
        if self.moveable and self.collide_mouse():
            self.view_y += 4
            self.check_down()
            return True
        return False

    def window_view_up(self):
        if self.moveable and self.collide_mouse():
            self.view_y -= 4
            self.check_down()
            return True
        return False

    def check_down(self):
        if self.view_y == max(0, self.content_height - self.height):
            self.down = True
        else:
            self.down = False


    def print_window(self):
        self.window.fill(self.background_color)
        pygame.draw.rect(self.window, color.BLACK, [0, 0, self.width, self.height], 1)

        self.update_content()
        self.print_content()

        self.manager.screen.blit(self.window, (self.x, self.y))
        self.clean()

    def clean(self):
        self.window.fill(self.background_color)

    def window_blit(self, content, x=0, y=0, loc=[], border_x=None, border_y=None):
        border_x = self.border_x if border_x is None else border_x
        border_y = self.border_y if border_y is None else border_y
        content_width, content_height = content.get_size()
        if "center" in loc:
            x, y = self.width / 2 - content_width / 2, self.height / 2 - content_height
        if "top" in loc:
            y = border_y
        if "bottom" in loc:
            y = self.height - content_height.height / 2 - border_y
        if "left" in loc:
            x = border_x
        if "right" in loc:
            x = self.width - content_width - border_x
        if "over" in loc:
            pygame.draw.rect(self.manager.screen, self.background_color,
                             [self.x, self.y + content_height, content_width, content_height])
            self.manager.screen.blit(content, (self.x, self.y + content_height))
            return None
        self.window.blit(content, (x, y))

    def update_extremum_view(self):
        self.view_x.set_max(0)
        self.view_y.set_max(max(0, self.content_height - self.content.get_size()[1]))

    def format_text(self, text, font, x_space=5, y_space=5):
        text_surface = pygame.Surface((self.width, self.height))
        text_surface.fill((0, 0, 0))
        space = font.size(' ')[0]
        line = font.size('I')[1]
        min_x, min_y = x_space, y_space
        max_x, max_y = self.width - x_space, self.height - y_space
        x, y = min_x, min_y
        for paragraph in text.split('\n'):
            for paragraph2 in paragraph.split('\t'):
                for word in paragraph2.split(' '):
                    rendered_word = self.font.render(word, 0, self.writing_color)
                    word_width = rendered_word.get_width()
                    if x + word_width >= max_x:
                        x = min_x
                        y += line
                    text_surface.blit(rendered_word, (x - self.view_x, y - self.view_y))

                    x += word_width + space
                x += 4 * space
            y += line
            x = min_x
        return text_surface, y

    def update_content(self):
        pass

    def print_content(self):
        if self.content is not None:
            self.window_blit(self.content)
        for button in self.buttons:
            button.display()

    def move(self, rel_x, rel_y):
        if self.moveable and self.collide_mouse():
            self.go_front()
            self.x += rel_x
            self.y += rel_y
            return True
        return False

    def go_front(self):
        if self.selectionable and self.manager.windows[-1] != self:
            self.manager.windows.remove(self)
            self.manager.windows.append(self)

    def close(self):
        if self.closable:
            if self.manager.windows[-1] == self:
                self.manager.windows.pop()
            else:
                self.manager.windows.remove(self)

    def new_button(self, button):
        self.buttons.add(button)
        self.controller.buttons.add(button)

    def erase_button(self, button):
        self.buttons.discard(button)
        self.controller.buttons.discard(button)

    def erase_buttons(self):
        for button in self.buttons:
            MultiButton.info[button.key] = None
            button.clicked = False
        self.buttons.clear()
        self.controller.buttons.clear()

    def select(self, x, y):
        if self.selectionable and self.collide(x, y):
            self.go_front()
            self.controller.activize()
            return True
        return False

    def retire_windows(self, *args):
        if self in self.manager.windows:
            self.manager.windows.remove(self)
        else:
            self.manager.add_debug(f"{type(self)} is already not in windows")
        self.controller.disable()
        self.add_retire_windows(*args)

    def add_retire_windows(self, *args):
        pass

    def add_windows(self, *args):
        self.manager.windows.append(self)
        self.controller.enable()
        self.add_add_windows(*args)

    def add_add_windows(self, *args):
        pass

    def set_window(self):
        for window in self.manager.windows:
            window.retire_windows()
        self.add_windows()



class MenuWindow(Window):
    def additionnal_init(self):
        self.start_button = Button(self, "center", 3 * self.height / 4 , "START", value=True, func_action=self.manager.start_main)
        self.new_button(self.start_button)

        self.auto_save_button = MultiButton(self, self.width / 5, "center", "AUTO SAVE", value="auto", key="import_histotree")
        self.crash_save_button = MultiButton(self, 2 * self.width / 5, "center", "CRASH SAVE", value="crash", key="import_histotree")
        self.select_save_button = MultiOptionButton(self, 3 * self.width / 5, "center", "SELECT SAVE", value="select", key="import_histotree", option_height=40, options=[file.name for file in self.manager.get_tree_files()], option_size=20)
        self.favorite_save_button = MultiButton(self, 4 * self.width / 5, "center", "FAVORITE SAVE", value="favorite", key="import_histotree", clicked=True)
        self.new_button(self.auto_save_button)
        self.new_button(self.crash_save_button)
        self.new_button(self.select_save_button)
        self.new_button(self.favorite_save_button)

    def add_add_windows(self):
        self.start_button.reset()


class MainWindow(Window):

    def additionnal_init(self):
        self.root_color = 230, 180, 80
        self.background_color = 10, 20, 15

    def update_content(self):
        self.content = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        for link in self.manager.histo_tree.links:

            pygame.draw.line(self.content, link.color if link != self.manager.selected else (255, 0, 0), self.manager.view(link.n1.pos), self.manager.view(link.n2.pos), int(5 * self.manager.zoom))
            angle = link.angle
            end = link.n2.x - math.cos(angle) * (link.n2.size - 3), link.n2.y - math.sin(angle) * (link.n2.size - 3)

            # Calculate the arrowhead points
            size = 20
            arrowhead1 = end[0] - size * math.cos(angle - math.pi / 6), end[1] - size * math.sin(angle - math.pi / 6)
            arrowhead2 = end[0] - size * math.cos(angle + math.pi / 6), end[1] - size * math.sin(angle + math.pi / 6)

            # Draw the arrowhead
            pygame.draw.polygon(self.content, link.color if link != self.manager.selected else (255, 0, 0), self.manager.list_view([end, arrowhead1, arrowhead2]))
        for node in self.manager.histo_tree.nodes:
            pygame.draw.circle(self.content, node.color if node != self.manager.selected else (255, 0, 0), self.manager.view(node.pos), node.size * self.manager.zoom)
        if self.manager.histo_tree.rooted():
            pygame.draw.circle(self.content, self.root_color, self.manager.view(self.manager.histo_tree.root.pos), self.manager.histo_tree.root.size * self.manager.zoom * 1.2, int(3 * self.manager.zoom))

        if self.manager.tool_controller.aux is not None:
            pygame.draw.circle(self.content, (180, 230, 150), self.manager.view(self.manager.tool_controller.aux.pos),
                               self.manager.tool_controller.aux.size * self.manager.zoom * 1.2, int(3 * self.manager.zoom))

    def add_add_windows(self):
        self.manager.view_home()
        self.manager.tool_window.mode = "main"
        self.manager.tool_window.add_windows()
        self.manager.map_controller.enable()


    def add_retire_windows(self):
        self.manager.tool_window.retire_windows()
        self.manager.map_controller.disable()


class ToolWindow(Window):

    height_button = 100

    def additionnal_init(self):
        self.mode = ""
        self.background_color = (100, 100, 100)

        self.link_button = MultiButton(self, self.width / 2, self.height_button * (0 + .5), "LINK", self.height_button, self.width, "link", key="main_tool")
        self.delete_button = MultiButton(self, self.width / 2, self.height_button * (1 + .5), "DELETE", self.height_button, self.width, "delete", key="main_tool")
        self.main_tools = {self.link_button, self.delete_button}

        self.link_to_button = MultiButton(self, self.width / 2, self.height_button * (0 + .5), "LINK", self.height_button, self.width, "link", key="node_tool")
        self.birth_button = MultiButton(self, self.width / 2, self.height_button * (1 + .5), "DESCENDANT", self.height_button, self.width, "birth", key="node_tool")
        self.type_button = MultiOptionButton(self, self.width / 2, self.height_button * (3 + .5), "TYPE", self.height_button, self.width, "type", ["Place", "Talk", "Fight"], option_height=30, key="node_tool")
        self.properties_tool = MultiButton(self, self.width / 2, self.height_button * (2 + .5), "PROPERTIES", self.height_button, self.width, "properties", key="node_tool", func_action=self.manager.properties_window.add_windows, func_inaction=self.manager.properties_window.retire_windows)
        self.node_tools = {self.link_to_button, self.birth_button, self.properties_tool, self.type_button}

        self.link_tools = set()

    def add_add_windows(self):
        match self.mode:
            case "main":
                button_list = self.main_tools
            case "node":
                button_list = self.node_tools
            case "link":
                button_list = self.link_tools
            case _:
                button_list = []
        for button in button_list:
            self.new_button(button)
        self.manager.debug_window.add_windows()

    def add_retire_windows(self):
        self.erase_buttons()
        self.manager.selection_controller.disable()
        self.manager.node_controller.disable()
        self.manager.link_controller.disable()
        self.manager.debug_window.retire_windows()


class DebugWindow(Window):

    def additionnal_init(self):
        self.text = ""
        self.down = True

    def update_content(self):
        if self.down:
            self.view_y.set_value(max(0, self.content_height - self.height))
        self.content, self.content_height = self.format_text(self.text, self.font)
        self.update_extremum_view()

    def add_text(self, text):
        self.text += text

    def set_down(self):
        if self.collide_mouse():
            self.down = True
            return True

    def clear_text(self):
        self.text = ""


class PropertiesWindow(Window):

    def additionnal_init(self):
        self.current_buttons = set()

        self.place_button = OptionButton(self, 400, 400, "Select a Place", 50, options=["Maison", "Chateau", "Temple"])
        self.place_buttons = {self.place_button}

        self.apply_button = Button(self, "center", "down", "APPLY", func_action=self.apply_func)
        self.new_button(self.apply_button)

    def apply_func(self):
        self.apply_button.reset()
        self.manager.add_debug("Changes Applied")
        # Apply changes


    def add_add_windows(self):
        self.manager.map_controller.disable()
        if self.manager.recognize_place():
            self.current_buttons = self.current_buttons.union(self.place_buttons)

    def add_retire_windows(self):
        self.manager.map_controller.enable()
        for button in self.current_buttons:
            self.erase_button(button)
        self.current_buttons.clear()



