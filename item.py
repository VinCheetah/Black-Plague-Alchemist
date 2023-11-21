import skills


class Item:

    def __init__(self, config):
        self.config = config
        self.name: str = self.config.name
        self.rarity: float = self.config.rarity
        self.description: str = self.config.description
        self.recipe: list[Item] = self.config.recipe


class Equipment(Item):

    def __init__(self, config):
        super().__init__(config)
        self.position: str = self.config.position  # where to put the equipment
        self.additional_skill: list[skills.Skill] = self.config.additional_skill


class Weapon(Item):

    def __init__(self, config):
        super().__init__(config)
        self.handiness: int = self.config.handiness  # one/two-handed
        self.direct_damage: (int, int) = self.config.direct_damage
        self.effects: list[skills.Skill] = self.config.effects


class Consumable(Item):

    def __init__(self, config):
        super().__init__(config)
        self.effects: list[skills.Skill] = self.config.effects


class Resource(Item):

    def __init__(self, config):
        super().__init__(config)
