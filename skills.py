import console


class Skill:

    def __init(self, game, config):
        self.game = game
        self.config = game.config.skill.basics | config
        self.name: str = self.config.name
        self.level: int = self.config.level


class FightSkill(Skill):

    def __init__(self, game, config):
        super().__init__(game, game.config.skill.fight.basics | config)
        self.action_consumption: int = self.config.action_consumption
        self.cooldown: int = self.config.cooldown
        self.mono_target = True
        self.target_type: str = self.config.target_type # self, enemy, ally, all
        self.target_number: int = self.config.target_number # [1, +inf]

    def applied(self, target):
        print(f"{self.name} have been applied to {target.name}")




class Perception:
    ...

class PotionCreation:
    ...

class Speed:
    ...




class Punch(FightSkill):

    def __init__(self, game):
        super().__init__(game, game.config.skill.fight.punch)


class SwordSlash:
    ...

class PotionThrow:
    ...


class Meteor(FightSkill):

    def __init__(self, game):
        super().__init__(game, game.config.skill.fight.meteor)
