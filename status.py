from object_classes import Status, FightStatus


class Neutral(Status):
    path = "neutral"


#####
# F #
# I #
# G #
# H #
# T #
#####

class Poisoned(FightStatus):
    path = "poisoned"


class Enraged(FightStatus):
    path = "enraged"


class Sleeping(FightStatus):
    path = "sleeping"


class Lucky(FightStatus):
    path = "lucky"


class Stunned(FightStatus):
    path = "stunned"


class Bleeding(FightStatus):
    path = "bleeding"


class Demotivated(FightStatus):
    path = "demotivated"




class Laughing(Status):
    ...


class Stunt(Status):
    ...


class Plagued(Status):
    ...


class Busy(Status):
    ...


class Motivated(Status):
    ...


class DeMotivated(Status):
    ...
