import random
from config import default_config
import place
import item
import random as rd


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

    def item_creation(self):
        for recipe in self.known_recipe:
            if self.check_ingredients(recipe, self.inventory):
                print(f"Create {recipe.product}")
