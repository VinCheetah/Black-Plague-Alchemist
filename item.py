import skills


class Item:

    def __init__(self, game, config):
        self.game = game
        self.config = game.config.item.basics | config
        self.name: str = self.config.name
        self.rarity: float = self.config.rarity
        self.description: str = self.config.description
        self.recipe: list[Item] = self.config.recipe


class Equipment(Item):

    def __init__(self, game, config):
        super().__init__(game, config)
        self.durability: float = self.config.durability
        self.position: str = self.config.position  # where to put the equipment
        self.additional_skill: list[skills.Skill] = self.config.additional_skill


class Weapon(Equipment):

    def __init__(self, game, config):
        super().__init__(game, config)
        self.direct_damage: (int, int) = self.config.direct_damage
        self.effects: list[skills.Skill] = self.config.effects


class Consumable(Item):

    def __init__(self, game, config):
        super().__init__(game, config)
        self.effects: list[skills.Skill] = self.config.effects


class Resource(Item):

    def __init__(self, game, config):
        super().__init__(game, config)


class Recipe(Item):

    def __init__(self, game, config):
        super().__init__(game, config)
        self.ingredients: list[(Item, int)] = self.config.ingredients
        self.products: list[(Item, int)] = self.config.products


class WoodStick(Resource):

    def __init__(self, game):
        super().__init__(game, game.config.item.resource.woodstick)


class Iron(Resource):

    def __init__(self, game):
        super().__init__(game, game.config.item.resource.iron)


class IronSword(Weapon):

    def __init__(self, game):
        super().__init__(game, game.config.item.equipment.weapon.ironsword)


class IronSwordRecipe(Recipe):

    def __init__(self, game):
        super().__init__(game, game.config.item.recipe.ironswordrecipe)
