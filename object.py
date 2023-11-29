

class Object:

    instances = set()

    def __init__(self, game, config):
        self.instances.add(self)
        self.game = game
        self.config = config
        self.config_initialized = False
        self.name = "Unknown object"

    def init_config(self):
        self.config_initialized = True

    def __repr__(self):
        return self.name
