import gameClass
import fight
import character


def simu_fight():

    new_game = gameClass.Game()

    new_fight = fight.Fight(new_game, {"player_team": [character.Alchemist(new_game)], "enemy_team": [character.Plagued(new_game)]})

    new_fight.start()

simu_fight()