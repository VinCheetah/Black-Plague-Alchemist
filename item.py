from object_classes import Item, Craftable, Equipment, Weapon, Consumable, Resource, Potion


class WoodStick(Resource):
    path = "wood_stick"


class Iron(Resource):
    path = "iron"


class IronSword(Weapon, Craftable):
    path = "iron_sword"


class WoodShield(Equipment, Craftable):
    path = "wood_shield"


class DamagePotion(Potion):
    path = "damage"


class HealPotion(Potion):
    path = "heal"

    def useful(self, fight, character) -> bool:
        return not fight.team_full_life(character, "ally")


class PoisonPotion(Potion):
    path = "poison"
