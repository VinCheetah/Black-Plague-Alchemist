from queue import PriorityQueue
from object_classes import FightSkill, FightingCharacter, PlayableCharacter, Monster
from config import MyDict
from gameClass import Game
from skills import FightSkill
import console
import random as rd


class Fight:

    def __init__(self, game: Game, config: MyDict | dict):
        self.game: Game = game
        self.slow = True
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

        for character in self.player_team:
            if isinstance(character, Monster):
                character.console_color = console.BLUE

    def start(self) -> None:
        console.say("Fight have started")
        while not self.fight_over:
            time, character = self.priority_queue.get_nowait()
            if character.is_defeated():
                continue
            if self.slow:
                input()
            console.print_fight(self)
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

    def request_target(self, skill: FightSkill, character: FightingCharacter) -> FightingCharacter:
        targets: list[FightingCharacter] = self.get_targets(skill, character)
        if self.game.io_mode == "console":
            return console.request("Choose your target :", targets)
        else:
            raise NotImplementedError

    def player_action(self, character: PlayableCharacter) -> tuple[FightSkill, FightingCharacter, list]:
        skill: FightSkill = character.request_fight_action()
        add_args = skill.fight_selected(self, character)
        target: FightingCharacter = skill.request_target(self, character, *add_args)
        return skill, target, add_args

    def enemy_action(self, character: FightingCharacter) -> tuple[FightSkill, FightingCharacter, list]:
        if self.enemy_tactic == "random":
            skill = rd.choice(character.fight_skill)
            target = rd.choice(self.get_targets(skill, character))
            return skill, target, []
        else:
            raise NotImplementedError

    def apply_damage_skill(self, skill, target: FightingCharacter, origin: FightingCharacter):
        target.get_damage(self.damage_attack(skill, target, origin))

    def apply_heal_skill(self, skill, target: FightingCharacter, origin: FightingCharacter):
        target.get_damage(-self.heal_attack(skill, target, origin))

    @staticmethod
    def heal_attack(skill, target: FightingCharacter, origin: FightingCharacter) -> int:
        target_heal_boost = target.compute_boost("heal", skill)
        origin_damage_boost = origin.compute_boost("damage", skill)
        return skill.heal * target_heal_boost * origin_damage_boost

    def damage_attack(self, skill, target: FightingCharacter, origin: FightingCharacter) -> int:
        if not self.is_dodged(skill, target, origin):
            target_defense_boost = target.compute_boost("defense", skill)
            origin_attack_boost = origin.compute_boost("damage", skill)
            critical_boost = self.critical_boost(skill, target, origin)
            return int(skill.damages * critical_boost / target_defense_boost * origin_attack_boost)
        else:
            console.say(f"{skill} made by {origin} on {target} is dodged !", "warning")
            return 0

    def is_dodged(self, skill, target, origin):
        target_dodge_boost = target.compute_boost("dodge", skill)
        origin_precision_boost = origin.compute_boost("precision", skill)
        return self.game.random_event(skill.dodge * target_dodge_boost / origin_precision_boost)

    def critical_boost(self, skill, target: FightingCharacter, origin: FightingCharacter) -> float:
        if self.is_critical(skill, target, origin):
            console.say(f"{skill} made by {origin} on {target} is critical !", "warning")
            target_defense_boost = target.compute_boost("critical_defense", skill)
            origin_attack_boost = origin.compute_boost("critical_damage", skill)
            return skill.critical_damage_boost * origin_attack_boost / target_defense_boost
        else:
            return 1

    def is_critical(self, skill, target: FightingCharacter, origin: FightingCharacter) -> bool:
        target_drop = target.compute_drop("critical_rate", skill)
        origin_boost = origin.compute_boost("critical_rate", skill)
        return self.game.random_event(skill.critical_rate * origin_boost / target_drop)

    def action(self, character: FightingCharacter) -> None:
        character.fight_statuses_update()
        if not character.attack_stop():
            skill, target, add_args = self.player_action(character) if isinstance(character, PlayableCharacter) else self.enemy_action(character)
            skill.applied(self, target, character, *add_args)
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




