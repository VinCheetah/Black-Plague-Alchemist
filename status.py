class Status:

    def __init__(self, config):
        self.config = config
        self.duration: int = self.config.duration #number of turns the status remains

class Neutral(Status):
    ...

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