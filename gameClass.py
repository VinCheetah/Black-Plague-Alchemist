import random

import character
import console
import status
from config import default_config
import place
import item
import random as rd


class Game:

    def __init__(self):
        self.config = default_config
        self.init_objects()
        self.main_character = []
        self.place = ...
        self.inventory: dict[item.Item, int] = self.config.general.inventory
        self.known_recipe: list[item.Recipe] = self.config.general.known_recipe
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
        self.iron_sword_recipe = item.IronSwordRecipe(self)

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

    def add_item(self, item, nb):
        if item not in self.inventory:
            self.inventory[item] = 0
        self.inventory[item] += nb

    def rm_item(self, item, nb):
        if item in self.inventory:
            self.inventory[item] -= nb
            if self.inventory[item] <= 0:
                del self.inventory[item]

    def check_ingredients(self, recipe, nb_prod):
        for (item, i) in recipe.ingredients:
            if item not in self.inventory or self.inventory[item] < i * nb_prod:
                return False
        return True

    def item_creation(self, nb_prod=1):
        for recipe in self.known_recipe:
            if self.check_ingredients(recipe, nb_prod):
                if self.io_mode == "console":
                    ans = console.answer_yn(f"Create {nb_prod} {recipe.product}? :")
                else:
                    raise NotImplementedError
                if ans:
                    for (item, i) in recipe.ingredients:
                        self.rm_item(item, i * nb_prod)
                    for (item, i) in recipe.products:
                        self.add_item(item, i * nb_prod)
                print(f"{recipe.product} have been created!")
