import gameClass
import fight
import character


def simu_fight():
    new_game = gameClass.Game()
    new_fight = fight.Fight(new_game, {"p"})

    new_fight.start()
