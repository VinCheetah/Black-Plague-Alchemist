from pathlib import Path

import pygame

pygame.init()
import button
import pickle
import os
from boundedValue import BoundedValue
from structure import Node, Link, HistoTree, PlaceNode, TalkNode, FightNode, ChoiceNode
import controllerClass
import window


class HistoTreeManager:
    def __init__(self):
        self.running: bool = False
        self.x: float = 0
        self.y: float = 0

        self.view_center_x: BoundedValue = BoundedValue(0)
        self.view_center_y: BoundedValue = BoundedValue(0)

        self.min_zoom: float = 0.1
        self.max_zoom: float = 10
        self.zoom: BoundedValue = BoundedValue(1, self.min_zoom, self.max_zoom)
        self.zoom_speed: float = 1.02

        self.histo_tree: HistoTree = HistoTree()
        self.default_file: str = "histotree/trees/histo_tree.pkl"
        self.auto_save_file: str = "histotree/trees/histo_auto_save.pkl"
        self.crash_file: str = "histotree/trees/histo_crash.pkl"
        self.favorite_file: str = "histotree/trees/favorite_save.pkl"

        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.display.set_caption("History Tree Designer")
        self.screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)

        self.width, self.height = self.screen.get_size()

        self.windows = []

        self.tool_size = 300
        self.debug_height = 500

        self.clock = pygame.time.Clock()

        self.controllers = list()
        self.insert_text_controller: controllerClass.InsertTextController = controllerClass.InsertTextController(self)
        self.properties_controller: controllerClass.PropertiesController = controllerClass.PropertiesController(self)
        self.debug_controller: controllerClass.DebugController = controllerClass.DebugController(self)
        self.tool_controller: controllerClass.ToolController = controllerClass.ToolController(self)
        self.node_controller: controllerClass.NodeController = controllerClass.NodeController(self)
        self.link_controller: controllerClass.LinkController = controllerClass.LinkController(self)
        self.selection_controller: controllerClass.SelectionController = controllerClass.SelectionController(self)
        self.map_controller: controllerClass.MapController = controllerClass.MapController(self)
        self.menu_controller: controllerClass.MenuController = controllerClass.MenuController(self)
        self.main_controller: controllerClass.MainController = controllerClass.MainController(self)

        self.properties_window: window.PropertiesWindow = window.PropertiesWindow(self, self.properties_controller, width=self.width - self.tool_size, height=self.height, x=self.tool_size)
        self.tool_window: window.ToolWindow = window.ToolWindow(self, self.tool_controller, width=self.tool_size, height=self.height - self.debug_height)
        self.menu_window: window.MenuWindow = window.MenuWindow(self, self.menu_controller, width=self.width, height=self.height)
        self.main_window: window.MainWindow = window.MainWindow(self, self.main_controller, width=self.width - self.tool_size, height=self.height, x=self.tool_size)
        self.debug_window: window.DebugWindow = window.DebugWindow(self, self.debug_controller, width=self.tool_size-10, height=self.debug_height-10, x=5, y =self.height-self.debug_height+5)

        self.menu_window.set_window()

        self.selected = None

        self.buildable = False
        self.moving_map = False
        self.move_map_anim = False
        self.hidden_tools = False

        self.mouse_pos = self.mouse_x, self.mouse_y = 0, 0


    def debug_window_view_up(self, *args):
        return self.debug_window.window_view_up()

    def debug_window_view_down(self, *args):
        return self.debug_window.window_view_down()

    def tool_window_view_up(self, *args):
        return self.tool_window.window_view_up()

    def tool_window_view_down(self, *args):
        return self.tool_window.window_view_down()

    def load(self, file_name) -> None:
        file = Path(file_name)
        if not file.parent.exists():
            file.parent.mkdir(parents=True)
        file.touch(exist_ok=True)
        with open(file, "rb") as f:
            self.histo_tree = pickle.load(f)
            self.update_tree()

    def favorite_save(self):
        self.save(self.favorite_file)

    def start_menu(self):
        self.save_auto_save()
        self.histo_tree = HistoTree()
        self.selected = None
        self.menu_window.set_window()

    def get_tree_files(self):
        return list((Path.cwd() / "histotree/trees").glob('*'))

    def start_main(self):
        if button.MultiButton.info["import_histotree"] is not None:
            match (button.MultiButton.info["import_histotree"][0]):
                case "auto":
                    self.load_auto_save()
                case "crash":
                    self.load_crash()
                case "select":
                    files = self.get_tree_files()
                    for file in files:
                        if file.name == button.MultiButton.info[button.MultiButton.info["import_histotree"][1].options[0].key][0]:
                            self.load(file.resolve())
                case "favorite":
                    self.load(self.favorite_file)

        self.main_window.set_window()
        self.add_debug("Should start")
        self.add_debug("Petite console de debug... essai \"p\"\n")

    def update_tree(self):
        new_histo_tree = HistoTree()
        update_dict = {}
        for node in self.histo_tree.nodes:
            update_dict[node] = new_histo_tree.add_node(*node.pos, type(node))
            self.histo_tree.transfer_info(update_dict[node], node)
        for link in self.histo_tree.links:
            new_histo_tree.add_link(update_dict[link.n1], update_dict[link.n2])
        if self.histo_tree.rooted():
            new_histo_tree.set_root(update_dict[self.histo_tree.root])
        self.histo_tree = new_histo_tree



    def save(self, file_name) -> None:
        file = Path(file_name)
        if not file.parent.exists():
            file.parent.mkdir(parents=True)
        file.touch(exist_ok=True)
        with open(file, "wb") as f:
            pickle.dump(self.histo_tree, f, pickle.HIGHEST_PROTOCOL)
        self.add_debug(f"{file_name} has been saved successfully !")

    def load_auto_save(self) -> None:
        self.load(self.auto_save_file)
        print("Auto save has been loaded")

    def load_histo_tree(self):
        file = input()
        file = self.default_file if file == "" else file
        self.load(file)

    def load_crash(self) -> None:
        self.load(self.crash_file)

    def save_auto_save(self) -> None:
        self.save(self.auto_save_file)

    def save_histo_tree(self) -> None:
        file = input()
        file = self.default_file if file == "" else file
        self.save(file)

    def save_crash(self):
        self.load(self.crash_file)

    def print_histo_tree(self) -> None:
        self.add_debug(str(self.histo_tree))

    def update_mouse_pos(self) -> None:
        self.mouse_pos = self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

    def anim(self):
        if self.move_map_anim:
            if abs(self.target_x - self.view_center_x) > 0.1 and abs(self.target_y - self.view_center_y) > 0.1:
                self.view_center_x += self.deca_x
                self.view_center_y += self.deca_y
            else:
                self.move_map_anim = False
                self.view_center_x = self.target_x
                self.view_center_y = self.target_y

    def add_debug(self, text) -> None:
        self.debug_window.add_text(str(text)+"\n")

    def interactions(self) -> None:
        self.update_mouse_pos()
        for event in pygame.event.get():
            translated_event = self.main_controller.translate(event)
            arg = []
            if translated_event is None:
                continue
            if type(translated_event) is tuple:
                translated_event, arg = translated_event
            for controller in self.controllers:
                if controller.apply(translated_event, *arg):
                    if controller.controller_debug:
                        print(f"I have applied {translated_event} with {controller.name}")
                    break
                elif controller.controller_debug:
                    print(f"Couldn't apply {translated_event} with {controller.name}")
            else:
                if translated_event is not None and self.main_controller.controller_debug:
                    print(f"Couldn't match event {translated_event}")

    def start(self):
        self.running = True

        while self.running:
            self.anim()
            self.display()
            self.interactions()
            pygame.display.flip()
            self.clock.tick(60)

    def screen_resize(self):
        self.width, self.height = self.screen.get_size()

    def add_controller(self, new_controller):
        self.controllers.append(new_controller)

    def select(self, selected):
        if self.selected is not None:
            self.unselect()

        self.selected = selected
        if isinstance(selected, Node):
            self.update_tools("node")
            self.node_controller.enable()
            self.update_buttons()
        elif isinstance(selected, Link):
            self.update_tools("link")
            self.link_controller.enable()
        self.selection_controller.enable()

    def update_buttons(self):
        self.tool_window.name_button.value = self.selected._name or ""
        self.tool_window.type_button.set_value(self.selected.type)
        if hasattr(self.selected.type, "place"):
            self.properties_window.place_button.set_value(self.selected.place)

    def change_node_type_selected(self):
        new_type = button.MultiButton.info[self.tool_window.type_button][0]
        translate_type = {"None": None, "Place": PlaceNode, "Talk": TalkNode, "Fight": FightNode, "Choice": ChoiceNode}.get(new_type)
        self.select(self.histo_tree.change_type_node(self.selected, translate_type))

    def update_tools(self, mode):
        if not self.hidden_tools:
            self.tool_window.retire_windows()
        self.tool_window.mode = mode
        self.tool_window.add_windows()
        if self.hidden_tools:
            self.tool_window.retire_windows()


    def unselect(self):
        if self.selected is not None:
            self.update_tools("main")
            if isinstance(self.selected, Node):
                self.node_controller.disable()
            elif isinstance(self.selected, Link):
                self.link_controller.disable()
            self.selection_controller.disable()
            self.selected = None
    def delete_selected(self):
        if self.selected is not None:
            if isinstance(self.selected, Node):
                self.histo_tree.delete_node(self.selected)
            elif isinstance(self.selected, Link):
                self.histo_tree.delete_link(self.selected)
            self.unselect()

    def selected_is_node(self):
        return self.selected is not None and isinstance(self.selected, Node)

    def display(self):
        self.screen.fill((0, 0, 0))
        for wind in self.windows:
            wind.print_window()

    def set_view_coord(self, x, y):
        self.view_center_x.set_value(x)
        self.view_center_y.set_value(y)

    def add_view_coord(self, x, y):
        self.view_center_x += x
        self.view_center_y += y

    def recognize_node(self, obj=None):
        return isinstance(obj or self.selected, Node)

    def recognize_link(self, obj=None):
        return isinstance(obj or self.selected, Link)

    def recognize_place(self, obj=None):
        return isinstance(obj or self.selected, PlaceNode)

    def move_map(self, rel_x, rel_y):
        if pygame.mouse.get_pressed()[0]:
            self.add_view_coord(- rel_x / self.zoom, - rel_y / self.zoom)
            self.buildable = False
            self.moving_map = True
            self.move_map_anim = False
            return True
        return False

    def zoom_move(self, *args):
        self.zoom *= self.zoom_speed
        return True

    def unzoom_move(self, *args):
        self.zoom /= self.zoom_speed
        return True

    def view_home(self):
        self.view_move(0, 0)

    def view_move(self, x, y):
        iter = 20
        self.move_map_anim = True
        self.target_x = x
        self.target_y = y
        self.deca_x = (self.target_x - self.view_center_x) / iter
        self.deca_y = (self.target_y - self.view_center_y) / iter


    def stop_running(self):
        self.running = False

    @staticmethod
    def dist(p1, p2):
        return pow(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2), 0.5)

    def view_x(self, x):
        return int((x - self.view_center_x) * self.zoom + self.main_window.width / 2)

    def view_y(self, y):
        return int((y - self.view_center_y) * self.zoom + self.main_window.height / 2)

    def view(self, p):
        return self.view_x(p[0]), self.view_y(p[1])

    def list_view(self, iterable):
        return [self.view(p) for p in iterable]

    def un_view_x(self, x):
        return (x - self.main_window.width / 2 - self.main_window.x) / self.zoom + self.view_center_x

    def un_view_y(self, y):
        return (y - self.main_window.height / 2 - self.main_window.y) / self.zoom + self.view_center_y

    def un_view(self, p):
        return self.un_view_x(p[0]), self.un_view_y(p[1])

    def dist_seg_point(self, p1, p2, p):
        if (p[0] - p1[0]) * (p2[0] - p1[0]) + (p[1] - p1[1]) * (p2[1] - p1[1]) <= 0:
            return self.dist(p1, p)
        if (p[0] - p2[0]) * (p1[0] - p2[0]) + (p[1] - p2[1]) * (p1[1] - p2[1]) <= 0:
            return self.dist(p2, p)
        return abs((p2[0] - p1[0]) * (p1[1] - p[1]) - (p1[0] - p[0]) * (p2[1] - p1[1])) / self.dist(p1, p2)