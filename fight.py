from queue import PriorityQueue
from object_classes import FightSkill, FightingCharacter, PlayableCharacter, Monster, Weapon
from config import MyDict
from gameClass import Game
from skills import FightSkill
import console
import random as rd


class Fight:
    def __init__(self, game: Game, config: MyDict | dict):
        self.game: Game = game
        self.config: MyDict = game.config.fight.basics | config
        self.slow: bool = self.config.slow
        self.escape_probability: float = self.config.escape_probability
        self.player_team: list[FightingCharacter] = self.config.player_team
        self.enemy_team: list[FightingCharacter] = self.config.enemy_team
        self.enemy_tactic: str = self.config.enemy_tactic
        self.player_team_size: int = len(self.player_team)
        self.enemy_team_size: int = len(self.enemy_team)
        self.dead_ally: list[FightingCharacter] = list()
        self.dead_enemy: list[FightingCharacter] = list()

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
            self.game.wait(0.5)
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

    def find_team(self, character: FightingCharacter, team_type):
        if team_type == "ally":
            return self.player_team if character in self.player_team else self.enemy_team
        elif team_type == "enemy":
            return self.enemy_team if character in self.player_team else self.player_team
        elif team_type == "all":
            return self.player_team + self.enemy_team

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

    def player_action(self, character: PlayableCharacter) -> tuple[FightSkill, FightingCharacter]:
        skill: FightSkill = character.request_fight_action()
        skill.fight_selected(self, character)
        target: FightingCharacter = skill.request_target(self, character,)
        return skill, target

    def enemy_action(self, character: FightingCharacter) -> tuple[FightSkill, FightingCharacter]:
        if self.enemy_tactic == "random":
            skill = rd.choice(character.fight_skill)
            target = rd.choice(self.get_targets(skill, character))
            return skill, target
        else:
            raise NotImplementedError

    def apply_damage_skill(self, skill: FightSkill | Weapon, target: FightingCharacter, origin: FightingCharacter):
        if not self.is_dodged(skill, target, origin):
            if skill.damages > 0:
                target.get_damage(self.damage_attack(skill, target, origin))
            skill.apply_effects(target)
        else:
            console.say(f"{skill} made by {origin} on {target} is dodged !", "fight_comment")

    def apply_heal_skill(self, skill, target: FightingCharacter, origin: FightingCharacter):
        target.get_heal(self.heal_attack(skill, target, origin))

    @staticmethod
    def heal_attack(skill, target: FightingCharacter, origin: FightingCharacter) -> int:
        target_heal_modifier = target.compute_tot_modifier("heal", skill)
        origin_damage_modifier = origin.compute_tot_modifier("damage", skill)
        return skill.heal * target_heal_modifier * origin_damage_modifier

    def damage_attack(self, skill, target: FightingCharacter, origin: FightingCharacter) -> int:
        target_defense_modifier = target.compute_tot_modifier("defense", skill)
        origin_attack_modifier = origin.compute_tot_modifier("damage", skill)
        critical_boost = self.critical_boost(skill, target, origin)
        return int(skill.damages * critical_boost / target_defense_modifier * origin_attack_modifier)

    def is_dodged(self, skill, target, origin):
        target_dodge_modifier = target.compute_tot_modifier("dodge", skill)
        origin_precision_modifier = origin.compute_tot_modifier("precision", skill)
        return self.game.random_event(skill.dodge * target_dodge_modifier / origin_precision_modifier)

    def critical_boost(self, skill, target: FightingCharacter, origin: FightingCharacter) -> float:
        if self.is_critical(skill, target, origin):
            console.say(f"{skill} made by {origin} on {target} is critical !", "fight_comment")
            target_defense_modifier = target.compute_tot_modifier("critical_defense", skill)
            origin_attack_modifier = origin.compute_tot_modifier("critical_damage", skill)
            return skill.critical_damage_boost * origin_attack_modifier / target_defense_modifier
        else:
            return 1

    def is_critical(self, skill, target: FightingCharacter, origin: FightingCharacter) -> bool:
        target_critical_rate_modifier = target.compute_tot_modifier("critical_rate", skill)
        origin_critical_rate_modifier = origin.compute_tot_modifier("critical_rate", skill)
        return self.game.random_event(skill.critical_rate * origin_critical_rate_modifier / target_critical_rate_modifier)

    def action(self, character: FightingCharacter) -> None:
        character.fight_statuses_update()
        if character.is_defeated():
            self.defeat_character(character)
        elif not character.attack_stop():
            skill, target = self.player_action(character) if isinstance(character, PlayableCharacter) else self.enemy_action(character)
            skill.applied(self, target, character)
            if target.is_defeated():
                self.defeat_character(target)

    def escape(self) -> None:
        if self.game.random_event(self.escape_probability):
            self.fight_over = True

    def defeat_character(self, character: FightingCharacter) -> None:
        console.say(f"{character} is defeated")
        team = self.player_team if character in self.player_team else self.enemy_team
        (self.dead_ally if character in self.player_team else self.dead_enemy).append(character)
        team.remove(character)
        character.fight_statuses = []
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
