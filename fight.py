class Fight:

    def __init__(self):
        self.player_team = ...
        self.enemy_team = ...


    def start_fight(self):
        while not self.fight_over:
            self.player_action()
            self.enemy_action()

    def player_action(self):
        ...

    def enemy_action(self):
        ...