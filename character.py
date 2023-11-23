import status
from boundedValue import BoundedValue
import skills
import item
import console


class Character:

    def __init__(self, game, config):
        self.game = game
        self.config = game.config.character.basics | config
        self.name = self.config.name


class FightingCharacter(Character):

    def __init__(self, game, config):
        super().__init__(game, game.config.character.fighter.basics | config)
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
        self.health: BoundedValue = BoundedValue(self.config.max_health, 0, self.config.max_health)
        self.equipment: dict[str, item.Equipment] = self.config.equipment
        # at most one equipment for each equipment slots
        self.basic_skill: dict[skills.Skill, int] = self.config.basic_skill
        self.social_links: dict[Character, int] = self.config.social_links
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
