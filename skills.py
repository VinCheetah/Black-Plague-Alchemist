from object import Object




class Skill(Object):

    def __init__(self, game, config):
        Object.__init__(self, game, game.config.skill.basics | config)

    def init_config(self):
        Object.init_config(self)
        self.name: str = self.config.name
        self.level: int = self.config.level




class FightSkill(Skill):

    def __init__(self, game, config):
        super().__init__(game, game.config.skill.fight.basics | config)

    def init_config(self):
        Skill.init_config(self)
        self.action_consumption: int = self.config.action_consumption
        self.cooldown: int = self.config.cooldown
        self.mono_target = True
        self.target_type: str = self.config.target_type  # self, enemy, ally, all
        self.target_number: int = self.config.target_number  # [1, +inf]
        self.damages: int = self.config.damages

    def applied(self, target):
        target.get_damage(self.damages)




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


class PotionThrow(FightSkill):

    def __init__(self, game):
        super().__init__(game, game.config.skill.fight.potion_throw)


class Meteor(FightSkill):

    def __init__(self, game):
        super().__init__(game, game.config.skill.fight.meteor)
