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

    def fight_selected(self, fight, character) -> list:
        if self.game.io_mode == "console":
            potion = console.request("Which potion would you like to throw:",
                            [item for item, num in self.game.inventory.items() if isinstance(item, Potion) and num > 0],
                            recommended_filter=lambda pot: pot.useful(fight, character),
                            valid_filter=lambda pot: pot.level_required(character))
            return [potion]
        else:
            raise NotImplementedError

    def request_target(self, fight, character, *add_args):
        assert len(add_args) == 1
        potion = add_args[0]
        return potion.find_target(fight, character)

    def applied(self, fight, target, origin, *add_args):
        assert len(add_args) == 1
        potion = add_args[0]
        potion.applied(fight, target, origin)
        self.exp_reward()


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
