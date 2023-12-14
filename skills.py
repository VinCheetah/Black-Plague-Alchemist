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
    path = "sword_slash"


class PotionThrow(FightSkill):
    path = "potion_throw"

    def fight_selected(self, fight, character) -> None:
        if self.game.io_mode == "console":
            self.weapon = console.request(
                "Which potion would you like to throw:",
                [item for item, num in self.game.inventory.items() if isinstance(item, Potion) and num > 0],
                recommended_filter=lambda pot: pot.useful(fight, character),
                valid_filter=lambda pot: pot.level_required(self),
            )
        else:
            raise NotImplementedError

    def request_target(self, fight, character):
        return self.weapon.find_target(fight, character)


class Curse(FightSkill):
    path = "curse"


class AngelBenediction(FightSkill):
    path = "angel_benediction"


class SatanClawStrike(FightSkill):
    path = "satan_claw_strike"


class Meteor(FightSkill):
    path = "meteor"


class HealPotion(FightSkill):
    path = "heal_potion"
