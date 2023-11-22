import random
from config import default_config
import place

import random as rd



class Game:

    def __init__(self):
        self.config = default_config
        self.main_character = []
        self.place = ...
        self.group_inventory = []
        self.characters = []

    def start(self):
        self.init_starting()

    def init_starting(self):
        self.place = place.Home()

    @staticmethod
    def random_event(probability):
        assert 0 <= probability <= 1
        return rd.random() < probability

