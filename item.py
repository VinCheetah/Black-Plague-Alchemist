import skills
from object import Object

class Item(Object):

    def __init__(self, game, config):
        Object.__init__(self, game, game.config.item.basics | config)

    def init_config(self):
        Object.init_config(self)
        self.name: str = self.config.name
        self.rarity: int = self.config.rarity
        self.description: str = self.config.description

    def __repr__(self):
        return self.name


class Craftable:

    def __init__(self, game, config):
        self.craftable_config = game.config.item.craftable.basics | config

    def init_config(self):
        self.known: bool = self.craftable_config.known
        self.recipe: dict[Item, int] = self.craftable_config._recipe


class Equipment(Item):

    def __init__(self, game, config):
        super().__init__(game, game.config.item.equipment.basics | config)

    def init_config(self):
        Item.init_config(self)
        self.durability: float = self.config.durability
        self.position: str = self.config.position  # where to put the equipment
        self.additional_skill: list[skills.Skill] = self.config.additional_skill


class Weapon(Equipment):

    def __init__(self, game, config):
        super().__init__(game, game.config.item.equipment.weapon.basics | config)

    def init_config(self):
        Equipment.init_config(self)
        self.min_damage: int = self.config.min_damage
        self.max_damage: int = self.config.max_damage
        self.effects: list[skills.Skill] = self.config.effects


class Consumable(Item):

    def __init__(self, game, config):
        super().__init__(game, game.config.item.consumable.basics | config)

    def init_config(self):
        Item.init_config(self)
        self.effects: list[skills.Skill] = self.config.effects


class Resource(Item):

    def __init__(self, game, config):
        super().__init__(game, game.config.item.resource.basics | config)


class WoodStick(Resource):

    def __init__(self, game):
        super().__init__(game, game.config.item.resource.wood_stick)


class Iron(Resource):

    def __init__(self, game):
        super().__init__(game, game.config.item.resource.iron)


class IronSword(Weapon, Craftable):

    def __init__(self, game):
        Weapon.__init__(self, game, game.config.item.equipment.weapon.iron_sword)
        Craftable.__init__(self, game, game.config.item.equipment.weapon.iron_sword)


    def init_config(self):
        Weapon.init_config(self)
        Craftable.init_config(self)




class WoodShield(Equipment, Craftable):

    def __init__(self, game):
        Equipment.__init__(self, game, game.config.item.equipment.wood_shield)
        Craftable.__init__(self, game, game.config.item.equipment.wood_shield)

    def init_config(self):
        Equipment.init_config(self)
        Craftable.init_config(self)






