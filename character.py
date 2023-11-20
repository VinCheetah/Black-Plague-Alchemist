import status
from boundedValue import BoundedValue
import skills
import item


class Character:

    def __init__(self, game, config):
        self.game = game
        self.config = config


class FightingCharacter(Character):

    def __init__(self, game, config):
        super().__init__(game, config)
        self.fight_skill: dict[skills.FightSkill, int] = self.config.fight_skill

    def request_fight_action(self):
        if self.game.io_mode == "console":
            print("Select an action\n -")
            print("\n - ".join(fight_skill.name for fight_skill in self.fight_skill))
            input
        else:
            raise NotImplementedError



class PlayableCharacter(Character):

    def __init__(self, config):
        super().__init__(config)
        self.config = {} | config
        self.health: BoundedValue = BoundedValue(self.config.max_health, 0, self.config.max_health)
        self.inventory: dict[item.Item, int] = self.config.inventory
        self.basic_skill: dict[skills.Skill, int] = self.config._basic_skill
        self.social_links: dict[Character, int] = self.config._social_links
        self.status: status.Status = ...


class Alchemist(Character):

    def __init__(self):
        super().__init__()


class Knight:
    ...

class Priest:
    ...

class Jester:
    ...




class SideCharacter(Character):
    ...

class Carpenter(SideCharacter):
    ...

class BlackSmith:
    ...

class Doctor:
    ...

class Peasant:
    ...

class Fanatic:
    ...

class Baron:
    ...




class Monster:
    ...

class Plagued(Monster):
    ...

class Dragon:
    ...

class PlaguedZombie:
    ...

class PlaguedDog:
    ...

class PlaguedRat:
    ...

class PlaguedSpider:
    ...
