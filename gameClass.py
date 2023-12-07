
import random as rd
from math import inf
import time

from object_classes import *
import character
import console
import status
import config
import place
import item
import skills


class Game:

    libs = [character, status, item, place, skills, console]

    def __init__(self):
        self.config = config.default_config
        self.io_mode = self.config.general.io_mode
        self.init_objects()
        self.link_config_game()
        self.init_config_all()
        self.main_character = []
        self.place = ...
        self.inventory: dict[Item, int] = self.config.general.inventory
        self.known_recipe: list[Craftable] = self.config.general.known_recipe
        self.characters = []

    def link_config_game(self):
        config.MyDict.game = self

    def init_config_all(self):
        while len(Object.non_init_instances) != 0:
            for obj in Object.non_init_instances:
                obj.init_config()
        assert len(Object.non_init_instances) == 0

    @staticmethod
    def wait(i):
        time.sleep(i)

    @staticmethod
    def list_product(iterable: list):
        prod = 1
        for element in iterable:
            prod *= element
        return prod

    def init_objects(self):
        self.init_characters()
        self.init_items()
        self.init_status()
        self.init_skills()
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
        self.wood_shield = item.WoodShield(self)
        self.poison_potion = item.PoisonPotion(self)
        self.heal_potion = item.HealPotion(self)
        self.damage_potion = item.DamagePotion(self)

    def init_status(self):
        self.neutral = status.Neutral(self)

    def init_skills(self):
        self.potion_throw = skills.PotionThrow(self)
        self.punch = skills.Punch(self)

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
            self.inventory[item] = 0
        self.inventory[item] += nb

    def add_recipe(self, item):
        if item in self.known_recipe:
            console.say(f"Recipe of {item.name} is already known", "warning")
        else:
            self.known_recipe.append(item)

    def rm_item(self, item, nb=1):
        if item in self.inventory:
            self.inventory[item] -= nb
            if self.inventory[item] <= 0:
                del self.inventory[item]

    def check_ingredients(self, recipe, nb_prod=1):
        for (item, i) in recipe.items():
            if item not in self.inventory or self.inventory[item] < i * nb_prod:
                console.say(f"Not enough *{item}*")
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
            chosen_item = console.request("Which recipe to perform? :", available_recipe)
            max_occ = self.max_available(chosen_item.recipe)
            chosen_occ = console.request_number(f"How many times to perform? :  [0 -- {max_occ}]", 0, max_occ)
            ans = console.answer_yn(f"Create {chosen_occ} {chosen_item}? :")
            if ans:
                for item, i in chosen_item.recipe.items():
                    self.rm_item(item, i * chosen_occ)
                self.add_item(chosen_item, chosen_occ)
                print(f"{chosen_occ} {chosen_item} have been created!")
            else:
                print("Nothing happened!")
        else:
            raise NotImplementedError
