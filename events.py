import character


class Events:

    def __init__(self, config):
        self.config = config
        self.name: str = self.config.name
        self.characters: list[character.Character] = self.config.characters


class MainEvents(Events):
    ...


class SecondaryEvents(Events):
    ...
