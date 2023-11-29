from boundedValue import BoundedValue
from object import Object
import status
import skills
import item
import console


class Character(Object):

    def __init__(self, game, config):
        Object.__init__(self, game, game.config.character.basics | config)

    def init_config(self):
        Object.init_config(self)
        self.name = self.config.name


class FightingCharacter(Character):

    def __init__(self, game, config):
        super().__init__(game, game.config.character.fighter.basics | config)

    def init_config(self):
        Character.init_config(self)
        self.fight_skill: list[skills.FightSkill] = self.config.fight_skill
        self.attack_rate: int = self.config.attack_rate

    def request_fight_action(self):
        if self.game.io_mode == "console":
            return self.fight_skill[console.request("Choose your next action :", self.fight_skill)]
        else:
            raise NotImplementedError


class PlayableCharacter(Character):

    def __init__(self, game, config):
        super().__init__(game, game.config.character.playable.basics | config)

    def init_config(self):
        Character.init_config(self)
        self.health: BoundedValue = BoundedValue(self.config.max_health, 0, self.config.max_health)
        self.equipment: dict[str, item.Equipment] = self.config.equipment  # at most one equipment for each equipment slots
        self.basic_skill: dict[skills.Skill, int] = self.config.basic_skill
        self.social_links: dict[Character, int] = self.config._social_links
        self.status: status.Status = self.config.status


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

    def __init__(self, game, config):
        super().__init__(game, game.config.character.monster.basics | config)

class Plagued(Monster):

    def __init__(self, game):
        super().__init__(game, game.config.character.monster.plagued)

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
