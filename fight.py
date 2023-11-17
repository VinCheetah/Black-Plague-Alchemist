from queue import PriorityQueue

class Fight:

    def __init__(self):
        self.fight_over = False
        self.player_team = ...
        self.enemy_team = ...
        self.priority_queue = PriorityQueue(self.player_team.get_size() + self.enemy_team.get_size())

    def start(self):
        while not self.fight_over:
            self.action(self.priority_queue.get())

    def player_action(self):
        ...

    def enemy_action(self):
        ...

    def action(self, character):
        if character in self.player_team:
            character.request_fight_action()
        elif character in self.enemy_team:
            character.take_fight_action()
        else:
            raise ValueError

    def escape(self):
        # With probability
        self.fight_over = True
