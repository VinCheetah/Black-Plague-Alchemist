import gameClass
import fight
import character
import item


def simu_fight():
    new_game = gameClass.Game()
    new_fight = fight.Fight(new_game, {"player_team": [new_game.alchemist, new_game.knight], "enemy_team": [character.Plagued.with_config(new_game), character.Plagued.with_config(new_game)]})
    new_fight.start()


# simu_fight()

def simu_creation():
    new_game = gameClass.Game()
    new_game.add_item(new_game.iron)
    new_game.add_item(new_game.wood_stick, 10)
    new_game.add_recipe(new_game.iron_sword)
    new_game.add_recipe(new_game.wood_shield)
    new_game.item_creation()


simu_creation()
