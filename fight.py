from queue import PriorityQueue
from object_classes import FightSkill, FightingCharacter, PlayableCharacter
from config import MyDict
from gameClass import Game
from skills import FightSkill
import console
import random as rd


class Fight:

    def __init__(self, game: Game, config: MyDict):
        self.game: Game = game
        self.config: MyDict = game.config.fight.basics | config
        self.escape_probability: float = self.config.escape_probability
        self.player_team: list[FightingCharacter] = self.config.player_team
        self.enemy_team: list[FightingCharacter] = self.config.enemy_team
        self.player_team_size: int = len(self.player_team)
        self.enemy_team_size: int = len(self.enemy_team)
        self.dead_ally: list[FightingCharacter] = list()
        self.dead_enemy: list[FightingCharacter] = list()
        self.enemy_tactic: str = self.config.enemy_tactic

        self.fight_over: bool = False
        self.priority_queue: PriorityQueue = PriorityQueue(len(self.player_team) + len(self.enemy_team))

        for character in self.enemy_team + self.player_team:
            self.priority_queue.put_nowait((character.attack_rate, character))

    def start(self) -> None:
        console.say("Fight have started")
        while not self.fight_over:
            console.print_fight(self)
            time, character = self.priority_queue.get_nowait()
            if character.is_defeated():
                continue
            self.game.wait(.5)
            character.say("My turn !")
            self.action(character)
            self.priority_queue.put_nowait((time + character.attack_rate, character))
        console.print_fight(self)
        console.say("Fight is over")
        self.result_fight()

    def result_fight(self) -> None:
        if len(self.player_team) == 0:
            console.say("You have been defeated")
        elif len(self.enemy_team) == 0:
            console.say("You won")
        else:
            print("Somebody escape...")

    def get_targets(self, skill: FightSkill, character) -> list[FightingCharacter]:
        if skill.mono_target and skill.target_type == "enemy":
            return self.enemy_team if character in self.player_team else self.player_team
        elif skill.mono_target and skill.target_type == "ally":
            return self.player_team if character in self.player_team else self.enemy_team
        else:
            raise NotImplementedError

    def request_target(self, skill, character: FightingCharacter) -> FightingCharacter:
        targets: list[FightingCharacter] = self.get_targets(skill, character)
        if self.game.io_mode == "console":
            return console.request("Choose your target :", targets)
        else:
            raise NotImplementedError

    def player_action(self, character: PlayableCharacter) -> tuple[FightSkill, FightingCharacter]:
        skill: FightSkill = character.request_fight_action()
        skill.fight_selected(self, character)
        target: FightingCharacter = self.request_target(skill, character)
        return skill, target

    def enemy_action(self, character: FightingCharacter) -> tuple[FightSkill, FightingCharacter]:
        if self.enemy_tactic == "random":
            skill = rd.choice(character.fight_skill)
            target = rd.choice(self.get_targets(skill, character))
            return skill, target
        else:
            raise NotImplementedError

    def action(self, character: FightingCharacter) -> None:
        skill, target = self.player_action(character) if isinstance(character, PlayableCharacter) else self.enemy_action(character)
        skill.applied(target)
        if target.is_defeated():
            self.defeat_character(target)

    def escape(self) -> None:
        if self.game.random_event(self.escape_probability):
            self.fight_over = True

    def defeat_character(self, character: FightingCharacter) -> None:
        console.say(f"{character} is defeated", "warning")
        team = self.player_team if character in self.player_team else self.enemy_team
        (self.dead_ally if character in self.player_team else self.dead_enemy).append(character)
        team.remove(character)
        if len(team) == 0:
            self.fight_over = True

    def team_full_life(self, character: FightingCharacter, team_type: str) -> bool:
        team: list[FightingCharacter]
        match team_type:
            case "ally":
                team = self.player_team if character in self.player_team else self.enemy_team
            case "enemy":
                team = self.enemy_team if character in self.player_team else self.player_team
            case _:
                raise ValueError
        for character in team:
            if character.health != character.health.max:
                return False
        return True




