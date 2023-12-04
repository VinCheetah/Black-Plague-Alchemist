import gameClass
import fight
import character
import item
import object

def simu_fight():
    new_game = gameClass.Game()
    new_game.add_item(new_game.poison_potion)
    new_game.add_item(new_game.heal_potion)
    new_game.add_item(new_game.damage_potion)
    new_fight = fight.Fight(new_game, {"player_team": [character.Plagued.with_config(new_game), new_game.alchemist], "enemy_team": [character.Plagued.with_config(new_game)]})
    new_fight.start()


simu_fight()


def simu_creation():
    new_game = gameClass.Game()
    new_game.add_item(new_game.iron)
    new_game.add_item(new_game.wood_stick, 10)
    new_game.add_recipe(new_game.iron_sword)
    new_game.add_recipe(new_game.wood_shield)
    new_game.item_creation()


# simu_creation()
