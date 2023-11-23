import gameClass
import fight
import character
import item

def simu_fight():
    new_game = gameClass.Game()
    new_fight = fight.Fight(new_game, {"player_team": [character.Alchemist(new_game)], "enemy_team": [character.Plagued(new_game)]})
    new_fight.start()


# simu_fight()

def simu_creation():
    new_game = gameClass.Game()
    new_game.add_item(item.Iron)
    new_game.add_item(item.WoodStick)
    new_game.add_item(item.IronSwordRecipe)
    new_game.item_creation()


simu_creation()
