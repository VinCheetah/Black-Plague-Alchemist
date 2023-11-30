from queue import PriorityQueue
from character import FightingCharacter, PlayableCharacter
from skills import FightSkill
import console
import random as rd


class Fight:

    def __init__(self, game, config):
        self.game = game
        self.config = game.config.fight.basics | config
        self.escape_probability = self.config.escape_probability
        self.player_team = self.config.player_team
        self.enemy_team = self.config.enemy_team
        self.player_team_size = len(self.player_team)
        self.enemy_team_size = len(self.enemy_team)
        self.dead_ally = list()
        self.dead_enemy = list()
        self.enemy_tactic = self.config.enemy_tactic

        self.fight_over = False
        self.priority_queue = PriorityQueue(len(self.player_team) + len(self.enemy_team))
        for character in self.enemy_team + self.player_team:
            self.priority_queue.put_nowait((character.attack_rate, character))

    def start(self):
        console.say("Fight have started")
        while not self.fight_over:
            console.print_fight(self)
            time, character = self.priority_queue.get_nowait()
            if character.is_defeated():
                continue
            character.say("My turn !")
            self.action(character)
            self.priority_queue.put_nowait((time + character.attack_rate, character))
        print("Fight is over")
        self.result_fight()


    def result_fight(self):
        if len(self.player_team) == 0:
            print("You have been defeated")
        else:
            print("You won")

    def get_targets(self, skill, character):
        if skill.mono_target and skill.target_type == "enemy":
            return self.enemy_team if character in self.player_team else self.player_team
        elif skill.mono_target and skill.target_type == "ally":
            return self.player_team if character in self.player_team else self.enemy_team
        else:
            raise NotImplementedError

    def request_target(self, skill, character: FightingCharacter):
        targets = self.get_targets(skill, character)
        if self.game.io_mode == "console":
            return targets[console.request("Choose your target :", targets)]
        else:
            raise NotImplementedError

    def player_action(self, character: PlayableCharacter) -> tuple[FightSkill, FightingCharacter]:
        skill = character.request_fight_action()
        target = self.request_target(skill, character)
        return skill, target

    def enemy_action(self, character: FightingCharacter) -> tuple[FightSkill, FightingCharacter]:
        if self.enemy_tactic == "random":
            skill = rd.choice(character.fight_skill)
            target = rd.choice(self.get_targets(skill, character))
            return skill, target
        else:
            raise NotImplementedError

    def action(self, character: FightingCharacter):
        skill, target = self.player_action(character) if isinstance(character, PlayableCharacter) else self.enemy_action(character)
        skill.applied(target)
        if target.is_defeated():
            self.defeat_character(target)


    def escape(self):
        if self.game.random_event(self.escape_probability):
            self.fight_over = True

    def defeat_character(self, character: FightingCharacter):
        print(f"{character} is defeated")
        team = self.player_team if isinstance(character, PlayableCharacter) else self.enemy_team
        team.remove(character)
        (self.dead_ally if isinstance(character, PlayableCharacter) else self.dead_enemy).append(character)
        if len(team) == 0:
            self.fight_over = True




