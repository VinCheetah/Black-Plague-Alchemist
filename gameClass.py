import random

import console
from config import default_config
import place
import item
import random as rd
from math import inf


class Game:

    def __init__(self):
        self.config = default_config
        self.main_character = []
        self.place = ...
        self.inventory: dict[item.Item, int] = self.config.general.inventory
        self.known_recipe: list[item.Recipe] = self.config.general.known_recipe
        self.characters = []

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

    def check_ingredients(self, recipe, nb_prod):
        for (item, i) in recipe.ingredients:
            if item not in self.inventory or self.inventory[item] < i * nb_prod:
                return False
        return True

    def max_available(self, recipe):
        max_occ = inf
        for (item, i) in recipe.ingredients:
            if item not in self.inventory:
                max_occ = 0
            else:
                max_occ = min(max_occ, self.inventory[item] // i)
        return max_occ

    def item_creation(self):
        available_recipe = [recipe for recipe in self.known_recipe if self.check_ingredients((recipe))]
        if self.io_mode == "console":
            chosen_recipe = available_recipe[console.request("Which recipe to perform? :", available_recipe)]
            max_occ = self.max_available(chosen_recipe)
            chosen_occ = console.request("How many times to perform? :", [i for i in range(max_occ + 1)])
            ans = console.answer_yn(f"Create {chosen_occ} {chosen_recipe.products}? :")
            if ans:
                for (item, i) in chosen_recipe.ingredients:
                    self.rm_item(item, i * chosen_occ)
                for (item, i) in chosen_recipe.products:
                    self.add_item(item, i * chosen_occ)
            print(f"{chosen_recipe.product} have been created!")
        else:
            raise NotImplementedError
