from object_classes import PlayableCharacter, SideCharacter, Monster


class Alchemist(PlayableCharacter):
    path = "alchemist"


class Knight(PlayableCharacter):
    path = "knight"


class Priest(PlayableCharacter):
    path = "priest"


class Jester(PlayableCharacter):
    path = "jester"


class Carpenter(SideCharacter):
    path = "carpenter"


class BlackSmith(SideCharacter):
    path = "blacksmith"


class Doctor(SideCharacter):
    path = "doctor"


class Peasant(SideCharacter):
    path = "peasant"


class Fanatic(SideCharacter):
    path = "fanatic"


class Baron(SideCharacter):
    path = "baron"


class Plagued(Monster):
    path = "plagued"


class Dragon(Monster):
    ...


class PlaguedZombie(Monster):
    ...


class PlaguedDog(Monster):
    ...


class PlaguedRat(Monster):
    ...


class PlaguedSpider(Monster):
    ...
