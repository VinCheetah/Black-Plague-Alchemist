import console
from object_classes import Skill, FightSkill
from object_classes import Potion




class Perception:
    ...

class PotionCreation:
    ...

class Speed:
    ...




class Punch(FightSkill):
    path = "punch"


class SwordSlash:
    ...


class PotionThrow(FightSkill):
    path = "potion_throw"

    def fight_selected(self, fight, character) -> None:
        if self.game.io_mode == "console":
            potion = console.request("Which potion would you like to throw:",
                            [item for item, num in self.game.inventory.items() if
                             isinstance(item, Potion) and num > 0],
                            recommended_filter=lambda pot: potion.useful(fight, character),
                            valid_filter=lambda pot: potion.level_required(character))
            potion.find_target()
        else:
            raise NotImplementedError


class Meteor(FightSkill):
    path = "meteor"


class HealPotion(FightSkill):
    path = "heal_potion"
