class Skill:

    def __init(self, config):
        self.config = config
        self.name: str = self.config.name
        self.level: int = self.config.level


class FightSkill(Skill):

    def __init__(self, config):
        super().__init__(config)
        self.action_consumption: int = self.config.action_consumption
        self.cooldown: int = self.config.cooldown

    def applied(self):
        print("skill have been applied")


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
