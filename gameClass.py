import random

import place

import random as rd

class Game:

    def __init__(self):
        self.main_character = []
        self.place = ...
        self.group_inventory = []
        self.characters = []

    def start(self):
        self.init_starting()

    def init_starting(self):
        self.place = place.Home()

    def random_event(self, probability):
        assert 0 <= probability <= 1
        return rd.random() < probability

