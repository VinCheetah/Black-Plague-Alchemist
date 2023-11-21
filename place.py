import character
import item
import events


class Place:

    def __init__(self, config):
        self.config = config
        self.name: str = self.config.name
        self.characters: list[character.Character] = self.config.characters
        self.items: dict[item.Item, float] = self.config.items
        # each item present has a "probability" (can be > 1) to be present
        self.adjacent_places: list[Place] = self.config.adjacent_places
        self.main_events: list[events.MainEvents] = self.config.main_events
        self.secondary_events: list[events.SecondaryEvents] = self.config.secondary_events


class Tavern(Place):
    ...


class Cave(Place):
    ...


class Castle(Place):
    ...


class Church(Place):
    ...


class DragonLair(Place):
    ...


class Dock:
    ...


class SkullIsland:
    ...


class Home:
    ...

    def introduction(self):
        print("my dad is zombie")
        print("i need kill dad")


class HomeVillage:
    ...


