

class Object:

    instances = list()

    def __init__(self, game, config):
        self.instances.append(self)
        self.game = game
        self.config = config
        self.config_initialized = False
        self.name = "Unknown object"

    def init_config(self):
        self.config_initialized = True

    def __repr__(self):
        return self.name

    @classmethod
    def with_config(cls, game):
        obj = cls(game)
        obj.init_config()
        obj.game.init_config_all()
        return obj

