from queue import PriorityQueue


class Fight:

    def __init__(self, game, config):
        self.game = game
        self.config = config
        self.fight_over = False
        self.escape_probability = self.config.escape_probability
        self.player_team = ...
        self.enemy_team = ...
        self.priority_queue = PriorityQueue(self.player_team.get_size() + self.enemy_team.get_size())

    def start(self):
        print("Fight have started")
        while not self.fight_over:
            self.action(self.priority_queue.get())
        print("Fight is over")

    def player_action(self, character):
        character.request_fight_action()

    def enemy_action(self, character):
        ...

    def action(self, character):
        if character in self.player_team:
            self.player_action(character)
        elif character in self.enemy_team:
            self.enemy_action(character)
        else:
            raise ValueError

    def escape(self):
        if self.game.random_event(self.escape_probability):
            self.fight_over = True
