import pygame

pygame.init()

import pickle
import os
from boundedValue import BoundedValue
from node import Node, HistoTree
import controllerClass


number = int | float


class HistoTreeManager:

    def __init__(self):
        self.running: bool = False
        self.x: number = 0
        self.y: number = 0

        self.view_center_x: number = 0
        self.view_center_y: number = 0

        self.min_zoom: number = .1
        self.max_zoom: number = 10
        self.zoom: BoundedValue = BoundedValue(1, self.min_zoom, self.max_zoom)

        self.histo_tree: HistoTree = HistoTree()
        self.default_file: str = "trees/histo_tree.pkl"
        self.auto_save_file: str = "trees/histo_auto_save.pkl"
        self.crash_file: str = "trees/histo_crash.pkl"

        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.display.set_caption("History Tree Designer")
        self.screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)

        self.width, self.height = self.screen.get_size()

        self.controllers = list()
        self.main_controller = controllerClass.MainController(self)

    def load(self, file) -> None:
        with open(file, "rb") as f:
            self.histo_tree = pickle.load(f)

    def save(self, file) -> None:
        with open(file, "wb") as f:
            pickle.dump(self.histo_tree, f, pickle.HIGHEST_PROTOCOL)

    def load_auto_save(self) -> None:
        self.load(self.auto_save_file)

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

    def update_mouse_pos(self) -> None:
        self.x, self.y = pygame.mouse.get_pos()

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
            self.display()
            self.interactions()
            pygame.display.flip()

    def screen_resize(self):
        self.height, self.width = self.screen.get_size()

    def add_controller(self, new_controller):
        self.controllers.append(new_controller)

    def display(self):
        pass

    def stop_running(self):
        self.running = False

    @staticmethod
    def dist(p1, p2):
        return pow(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2), .5)

    def view_x(self, x):
        return int((x - self.view_center_x) * self.zoom + self.width / 2)

    def view_y(self, y):
        return int((y - self.view_center_y) * self.zoom + self.height / 2)

    def view(self, p):
        return self.view_x(p[0]), self.view_y(p[1])

    def un_view_x(self, x):
        return (x - self.width / 2) / self.zoom + self.view_center_x

    def un_view_y(self, y):
        return (y - self.height / 2) / self.zoom + self.view_center_y

    def un_view(self, p):
        return self.un_view_x(p[0]), self.un_view_y(p[1])

    def dist_seg_point(self, p1, p2, p):
        if (p[0] - p1[0]) * (p2[0] - p1[0]) + (p[1] - p1[1]) * (p2[1] - p1[1]) <= 0:
            return self.dist(p1, p)
        if (p[0] - p2[0]) * (p1[0] - p2[0]) + (p[1] - p2[1]) * (p1[1] - p2[1]) <= 0:
            return self.dist(p2, p)
        return abs((p2[0] - p1[0]) * (p1[1] - p[1]) - (p1[0] - p[0]) * (p2[1] - p1[1])) / self.dist(p1, p2)


debug = True
manager = HistoTreeManager()

try:
    manager.start()
except:
    if debug:
        pass  # Debug Checkpoint
    manager.save_crash()
    raise
