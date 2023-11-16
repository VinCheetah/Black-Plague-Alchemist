import status



class Character:

    def __init__(self, config):
        self.health : int = ...
        self.inventory = ...
        self.fight_skill = config.fight_skill
        self.basic_skill = config.basic_skill
        self.social_links: dict[Character, int] = {}
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
