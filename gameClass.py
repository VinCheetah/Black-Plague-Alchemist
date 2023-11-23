import random

import character
import console
import status
from config import default_config
import place
import item
import random as rd
from math import inf


class Game:

    def __init__(self):
        self.config = default_config
        self.io_mode = "console"
        self.init_objects()
        self.main_character = []
        self.place = ...
        self.inventory: dict[item.Item, int] = self.config.general.inventory
        self.known_recipe: list[item.Craftable] = self.config.general.known_recipe
        self.characters = []

    def init_objects(self):
        self.init_characters()
        self.init_items()
        self.init_status()
        # self.init_place()
        # self.init_status()

    def init_characters(self):
        self.alchemist = character.Alchemist(self)
        self.knight = character.Knight(self)

        self.plagued = character.Plagued(self)

    def init_items(self):
        self.wood_stick = item.WoodStick(self)
        self.iron = item.Iron(self)
        self.iron_sword = item.IronSword(self)

    def init_status(self):
        self.neutral = status.Neutral(self)

    def start(self):
        self.init_starting()

    def init_starting(self):
        self.place = place.Home()

    @staticmethod
    def random_event(probability):
        assert 0 <= probability <= 1
        return rd.random() < probability

    def add_item(self, item, nb=1):
        if item not in self.inventory:
            print(type(self.inventory))
            self.inventory[item] = 0
        self.inventory[item] += nb

    def rm_item(self, item, nb=1):
        if item in self.inventory:
            self.inventory[item] -= nb
            if self.inventory[item] <= 0:
                del self.inventory[item]

    def check_ingredients(self, recipe, nb_prod=1):
        for (item, i) in recipe.items():
            if item not in self.inventory or self.inventory[item] < i * nb_prod:
                return False
        return True

    def max_available(self, recipe):
        max_occ = inf
        for (item, i) in recipe.items():
            if item not in self.inventory:
                max_occ = 0
            else:
                max_occ = min(max_occ, self.inventory[item] // i)
        return max_occ

    def item_creation(self):
        available_recipe = [item for item in self.known_recipe if self.check_ingredients(item.recipe)]
        if self.io_mode == "console":
            chosen_item = available_recipe[console.request("Which recipe to perform? :", available_recipe)]
            max_occ = self.max_available(chosen_item.recipe)
            chosen_occ = console.request("How many times to perform? :", [i for i in range(max_occ + 1)])
            ans = console.answer_yn(f"Create {chosen_occ} {chosen_item}? :")
            if ans:
                for (item, i) in chosen_item.recipe:
                    self.rm_item(item, i * chosen_occ)
                self.add_item(chosen_item, * chosen_occ)
            print(f"{chosen_occ} {chosen_item} have been created!")
        else:
            raise NotImplementedError
