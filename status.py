class Status:

    def __init__(self, game, config):
        self.game = game
        self.config = game.config.status.basics | config
        self.duration: int = self.config.duration #number of turns the status remains

class Neutral(Status):

    def __init__(self, game):
        super().__init__(game, game.config.status.neutral)


class Laughing(Status):
    ...

class Bleeding(Status):
    ...

class Stunt(Status):
    ...

class Poisonned(Status):
    ...

class Plagued(Status):
    ...

class Busy(Status):
    ...

class Sleeping(Status):
    ...

class Motivated(Status):
    ...

class DeMotivated(Status):
    ...