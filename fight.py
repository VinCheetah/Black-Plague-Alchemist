from queue import PriorityQueue
import console
import random as rd


class Fight:

    def __init__(self, game, config):
        self.game = game
        self.config = game.config.fight.basics | config
        self.escape_probability = self.config.escape_probability
        self.player_team = self.config.player_team
        self.enemy_team = self.config.enemy_team
        self.enemy_tactic = self.config.enemy_tactic

        self.fight_over = False
        self.priority_queue = PriorityQueue(len(self.player_team) + len(self.enemy_team))
        for character in self.enemy_team:
            self.priority_queue.put_nowait((character.attack_rate, character))

    def start(self):
        print("Fight have started")
        while not self.fight_over:
            time, character = self.priority_queue.get_nowait()
            print(f"{character.name} is doing an action")
            self.action(character)
            self.priority_queue.put_nowait((time + character.attack_rate, character))
        print("Fight is over")

    def get_targets(self, skill, character):
        if skill.mono_target and skill.target_type == "enemy":
            return self.enemy_team if character in self.player_team else self.player_team
        elif skill.mono_targert and skill.target_type == "ally":
            return self.player_team if character in self.player_team else self.enemy_team
        else:
            raise NotImplementedError

    def request_target(self, skill, character):
        targets = self.get_targets(skill, character)
        if self.game.io_mode == "console":
            return targets[console.request("Choose your target :", targets)]
        else:
            raise NotImplementedError

    def player_action(self, character):
        skill = character.request_fight_action()
        target = self.request_target(skill, character)
        skill.applied(target)

    def enemy_action(self, character):
        if self.enemy_tactic == "random":
            skill = rd.choice(character.fight_skill)
            target = rd.choice(self.get_targets(skill, character))
            skill.applied(target)
        else:
            raise NotImplementedError

    def action(self, character):
        if character in self.player_team:
            self.player_action(character)
        elif character in self.enemy_team:
            self.enemy_action(character)
        else:
            raise NotImplementedError

    def escape(self):
        if self.game.random_event(self.escape_probability):
            self.fight_over = True
