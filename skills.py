import console

class Skill:

    def __init(self, game, config):
        self.game = game
        self.config = config
        self.name: str = self.config.name
        self.level: int = self.config.level


class FightSkill(Skill):

    def __init__(self, config):
        super().__init__(config)
        self.action_consumption: int = self.config.action_consumption
        self.cooldown: int = self.config.cooldown

    def applied(self, target):
        print(f"{self.name} have been applied to {target.name}")




class Perception:
    ...

class PotionCreation:
    ...

class Speed:
    ...





class SwordSlash:
    ...

class PotionThrow:
    ...
