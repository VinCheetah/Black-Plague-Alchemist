import status
from boundedValue import BoundedValue
import skills
import item
import console


class Character:

    def __init__(self, game, config):
        self.game = game
        self.config = game.config.character.basics | config


class FightingCharacter(Character):

    def __init__(self, game, config):
        super().__init__(game, game.config.fighter.basics | config)
        self.fight_skill: list[skills.FightSkill] = self.config.fight_skill

    def request_fight_action(self):
        if self.game.io_mode == "console":
            self.fight_skill[console.request("Choose your next action :", self.fight_skill)].applied()
        else:
            raise NotImplementedError


class PlayableCharacter(Character):

    def __init__(self, game, config):
        super().__init__(game, game.config.playable.basics | config)
        self.health: BoundedValue = BoundedValue(self.config.max_health, 0, self.config.max_health)
        self.inventory: dict[item.Item, int] = self.config.inventory
        self.basic_skill: dict[skills.Skill, int] = self.config.basic_skill
        self.social_links: dict[Character, int] = self.config.social_links
        self.status: status.Status = ...


class Alchemist(PlayableCharacter):

    def __init__(self, game):
        super().__init__(game, game.config.character.playable.alchemist)


class Knight(PlayableCharacter):

    def __init__(self, game):
        super().__init__(game, game.config.character.playable.knight)


class Priest(PlayableCharacter):

    def __init__(self, game):
        super().__init__(game, game.config.character.playable.priest)


class Jester(PlayableCharacter):

    def __init__(self, game):
        super().__init__(game, game.config.character.playable.jester)



class SideCharacter(FightingCharacter):
    ...

class Carpenter(SideCharacter):
    ...

class BlackSmith(SideCharacter):
    ...

class Doctor(SideCharacter):
    ...

class Peasant(SideCharacter):
    ...

class Fanatic(SideCharacter):
    ...

class Baron(SideCharacter):
    ...




class Monster(FightingCharacter):
    ...

class Plagued(Monster):
    ...

class Dragon(Monster):
    ...

class PlaguedZombie(Monster):
    ...

class PlaguedDog(Monster):
    ...

class PlaguedRat(Monster):
    ...

class PlaguedSpider(Monster):
    ...
