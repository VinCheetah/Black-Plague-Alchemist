from object_classes import Item, Craftable, Equipment, Weapon, Consumable, Resource, Potion


class WoodStick(Resource):
    path = "wood_stick"


class Iron(Resource):
    path = "iron"


class IronSword(Equipment, Weapon, Craftable):
    path = "iron_sword"


class WoodShield(Equipment, Craftable):
    path = "wood_shield"


class DamagePotion(Potion):
    path = "damage"


class HealPotion(Potion):
    path = "heal"


class PoisonPotion(Potion):
    path = "poison"
