import console
from boundedValue import BoundedValue
from config import MyDict, default_config
from typing import Any, Type


class Object:
    instances = list()
    non_init_instances = list()

    def __init__(self, game, config):
        self.instances.append(self)
        self.non_init_instances.append(self)
        self.game = game
        self.config = config
        self.config_initialized = False
        self.name = "Unknown object"

        if isinstance(self, FightModifier):
            FightModifier.__init__(self)

    def init_config(self):
        self.name = self.config.name
        if not self.config_initialized:
            self.non_init_instances.remove(self)
            self.config_initialized = True
        else:
            print(f"{self.name} got initalized again")

    def __repr__(self):
        if hasattr(self, "console_color"):
            return self.console_color + self.name + console.RESET_ALL
        return self.name

    @classmethod
    def with_config(cls, game):
        obj = cls(game)
        obj.game.init_config_all()
        return obj


class FightModifier:

    def __init__(self):
        if hasattr(self, "config"):
            self.config |= default_config.fight_modifier.basics
            self.stop_attack: bool = self.config.stop_attack
            self.attack_rate_boost: float = self.config.attack_rate_boost
            self.attack_rate_drop: float = self.config.attack_rate_drop
            self.precision_boost: float = self.config.precision_boost
            self.precision_drop: float = self.config.precision_drop
            self.damage_boost: float = self.config.damage_boost
            self.damage_drop: float = self.config.damage_drop
            self.defense_boost: float = self.config.defense_boost
            self.defense_drop: float = self.config.defense_drop
            self.heal_boost: float = self.config.heal_boost
            self.heal_drop: float = self.config.heal_drop
            self.critical_damage_boost: float = self.config.critical_damage_boost
            self.critical_damage_drop: float = self.config.critical_damage_drop
            self.critical_defense_boost: float = self.config.critical_defense_boost
            self.critical_defense_drop: float = self.config.critical_defense_drop
            self.critical_rate_boost: float = self.config.critical_rate_boost
            self.critical_rate_drop: float = self.config.critical_rate_drop
            self.dodge_boost: float = self.config.dodge_boost
            self.dodge_drop: float = self.config.dodge_drop
        else:
            console.say(f"Fight Modifier without config", "warning")

    def compute_modifier(self, attr):
        boost = getattr(self, attr + "_boost")
        drop = getattr(self, attr + "_drop")
        if True:
            if boost != 1:
                console.say(f"{self} have boost {attr} for {boost}", "warning")
            if drop != 1:
                console.say(f"{self} have drop {attr} for {drop}", "warning")
        return boost / drop


class Skill(Object):
    def __init__(self, game, prev_config=None):
        class_config = default_config.skill
        config = prev_config if prev_config is not None else MyDict()
        if hasattr(self, "path"):
            if self.path is not None:
                if self.path in class_config:
                    config |= class_config[self.path]
                    self.path = None
                else:
                    console.say(f"Should have {self.path} in {class_config}", "warning")
        else:
            console.say(f"{type(self)} do not have path")
        config |= class_config.basics
        super().__init__(game, config)

    def init_config(self):
        super().init_config()
        self.name: str = self.config.name
        self.level: int = self.config.level

    def train(self) -> None:
        self.level += 1

    def selected(self) -> None:
        pass


class FightSkill(Skill, Object):
    def __init__(self, game, prev_config=None):
        class_config = default_config.skill.fight
        config = prev_config if prev_config is not None else MyDict()
        if hasattr(self, "path"):
            if self.path is not None:
                if self.path in class_config:
                    config |= class_config[self.path]
                else:
                    console.say(f"Should have {self.path} in {class_config}", "warning")
                self.path = None
        else:
            console.say(f"{type(self)} do not have path")
        config |= class_config.basics
        super().__init__(game, config)

    def init_config(self):
        super().init_config()
        self.use_weapon: bool = self.config.use_weapon
        self.effects: dict[Type[FightStatus], float] = self.config._effects
        self.action_consumption: int = self.config.action_consumption
        self.cooldown: int = self.config.cooldown
        self.mono_target = True
        self.target_type: str = self.config.target_type  # self, enemy, ally, all
        self.target_number: int = self.config.target_number  # [1, +inf]
        self.damages: int = self.config.damages
        self.heal: int = self.config.heal
        self.dodge: float = self.config.dodge
        self.critical_rate: float = self.config.critical_rate
        self.critical_damage_boost: float = self.config.critical_damage_boost
        self.weapon: Weapon | None = None

    def applied(self, fight, target, origin):
        self.exp_reward()
        if self.use_weapon:
            assert self.weapon is not None
            self.weapon.applied(fight, target, origin)
            self.weapon = None
        else:
            console.say(f"{origin} used {self} on {target}")
            if self.damages > 0 or len(self.effects) > 0:
                fight.apply_damage_skill(self, target, origin)
            if self.heal > 0:
                fight.apply_heal_skill(self, target, origin)

    def apply_effects(self, target):
        for effect, probability in self.effects.items():
            if self.game.random_event(probability):
                target.get_fight_status(effect.with_config(self.game))

    def exp_reward(self):
        pass

    def train(self):
        super().train()
        self.damages *= 1.5

    def fight_selected(self, fight, character) -> None:
        pass

    def request_target(self, fight, character):
        return fight.request_target(self, character)




class Character(Object):
    def __init__(self, game, prev_config=None):
        class_config = default_config.character
        config = prev_config if prev_config is not None else MyDict()
        if hasattr(self, "path"):
            if self.path is not None:
                if self.path in class_config:
                    config |= class_config[self.path]
                    self.path = None
                else:
                    console.say(f"Should have {self.path} in {class_config}", "warning")
        else:
            console.say(f"{type(self)} do not have path")
        config |= class_config.basics
        super().__init__(game, config)

    def init_config(self):
        Object.init_config(self)
        self.name = self.config.name
        self.console_color = self.config.console_color
        self.statuses = self.config.statuses

    def say(self, what, bold=True, end="\n", map_what=True):
        console.say(what, self, bold, end, map_what)

    def add_status(self, status):
        console.say(f"{self.name} is now {status}", "warning")


class FightingCharacter(Character, FightModifier):
    def __init__(self, game, prev_config=None):
        class_config = default_config.character.fighter
        config = prev_config if prev_config is not None else MyDict()
        if hasattr(self, "path"):
            if self.path is not None:
                if self.path in class_config:
                    config |= class_config[self.path]
                    self.path = None
                else:
                    console.say(f"Should have {self.path} in {class_config}", "warning")
        else:
            console.say(f"{type(self)} do not have path")
        config |= class_config.basics
        super().__init__(game, config)

        self.fight_statuses: list = []
        self.new_fight_statuses: list = []

    def init_config(self):
        super().init_config()
        self.fight_skill: list[FightSkill] = self.config.fight_skill
        self.attack_rate: int = self.config.attack_rate
        self.health: BoundedValue = BoundedValue(self.config.max_health, 0, self.config.max_health)
        self.equipments: list = self.config.equipments

    def get_damage(self, damages):
        console.say(console.RED + f"{damages} damages on {self}" + console.RESET_ALL)
        self.health -= damages

    def get_heal(self, heal):
        console.say(console.GREEN + f"{heal} heals on {self} " + console.RESET_ALL)
        self.health += heal

    def compute_tot_modifier(self, attr, skill):
        return (
            self.compute_modifier(attr)
            * self.game.list_product([fs.compute_modifier(attr) for fs in self.fight_statuses])
            * self.game.list_product([equip.compute_modifier(attr) for equip in self.equipments])
            * self.game.list_product([status.compute_modifier(attr) for status in self.statuses])
        )
        # Could add modifier linked to skill

    def fight_statuses_update(self):
        for status in self.fight_statuses:
            status.duration -= 1
            if status.damages > 0 and self.game.random_event(status.damages_rate):
                self.get_damage(status.damages)
            if status.heal > 0:
                self.get_heal(status.heal)
            if status.duration == 0:
                self.fight_statuses.remove(status)
        for new_status in self.new_fight_statuses:
            self.get_fight_status(new_status)
        self.new_fight_statuses = []

    def get_fight_status_delayed(self, status):
        self.new_fight_statuses.append(status)

    def get_fight_status(self, new_status):
        console.say(f"{self} is now {new_status} for {new_status.duration} turns !", "fight_comment")
        for fs in self.fight_statuses:
            if type(fs) is type(new_status):
                self.fight_statuses.remove(fs)
        self.fight_statuses.append(new_status)

    def attack_stop(self):
        for status in self.fight_statuses:
            if status.stop_attack:
                console.say(f"{self} is {status}, and so cannot attack", "fight_comment")
                return True
        return False

    def is_defeated(self):
        return self.health == 0

    def __lt__(self, other):
        return self.health < other.health


class PlayableCharacter(FightingCharacter):
    def __init__(self, game, prev_config=None):
        class_config = default_config.character.playable
        config = prev_config if prev_config is not None else MyDict()
        if hasattr(self, "path"):
            if self.path is not None:
                if self.path in class_config:
                    config |= class_config[self.path]
                    self.path = None
                else:
                    console.say(f"Should have {self.path} in {class_config}", "warning")
        else:
            console.say(f"{type(self)} do not have path")
        config |= class_config.basics
        super().__init__(game, config)

    def init_config(self):
        super().init_config()
        self.basic_skill: dict[Skill, int] = self.config._basic_skill
        self.social_links: dict[Character, int] = self.config._social_links
        self.status: Status = self.config.status

    def request_fight_action(self):
        if self.game.io_mode == "console":
            return console.request("Choose your next action :", self.fight_skill)
        else:
            raise NotImplementedError


class SideCharacter(FightingCharacter):
    def __init__(self, game, prev_config=None):
        class_config = default_config.character.side
        config = prev_config if prev_config is not None else MyDict()
        if hasattr(self, "path"):
            if self.path is not None:
                if self.path in class_config:
                    config |= class_config[self.path]
                    self.path = None
                else:
                    console.say(f"Should have {self.path} in {class_config}", "warning")
        else:
            console.say(f"{type(self)} do not have path")
        config |= class_config.basics
        super().__init__(game, config)

    def init_config(self):
        super().init_config()


class Monster(FightingCharacter):
    def __init__(self, game, prev_config=None):
        class_config = default_config.character.monster
        config = prev_config if prev_config is not None else MyDict()
        if hasattr(self, "path"):
            if self.path is not None:
                if self.path in class_config:
                    config |= class_config[self.path]
                    self.path = None
                else:
                    console.say(f"Should have {self.path} in {class_config}", "warning")
        else:
            console.say(f"{type(self)} do not have path")
        config |= class_config.basics
        super().__init__(game, config)

    def init_config(self):
        super().init_config()

        #

    ###
    #####
    #######
    #########






class Item(Object):
    def __init__(self, game, prev_config=None):
        class_config = default_config.item
        config = prev_config if prev_config is not None else MyDict()
        if hasattr(self, "path"):
            if self.path is not None:
                if self.path in class_config:
                    config |= class_config[self.path]
                    self.path = None
                else:
                    console.say(f"Should have {self.path} in {class_config}", "warning")
        else:
            console.say(f"{type(self)} do not have path", "warning")
        config |= class_config.basics
        super().__init__(game, config)

        if isinstance(self, Craftable):
            Craftable.__init__(self)
        if isinstance(self, Weapon):
            Weapon.__init__(self)

    def init_config(self):
        super().init_config()
        self.name: str = self.config.name
        self.rarity: int = self.config.rarity
        self.description: str = self.config.description

        if isinstance(self, Craftable):
            Craftable.init_config(self)

        if isinstance(self, Weapon):
            Weapon.init_config(self)


class Craftable:
    def __init__(self):
        if hasattr(self, "config") and hasattr(self, "game"):
            self.config |= self.game.config.item.craftable.basics
        else:
            console.say(f"Craftable without config/game", "warning")

    def init_config(self):
        self.known: bool = self.config.known
        self.recipe: dict[Item, int] = self.config._recipe


class Equipment(Item, FightModifier):
    def __init__(self, game, prev_config=None):
        class_config = default_config.item.equipment
        config = prev_config if prev_config is not None else MyDict()
        if hasattr(self, "path"):
            if self.path is not None:
                if self.path in class_config:
                    config |= class_config[self.path]
                    self.path = None
                else:
                    console.say(f"Should have {self.path} in {class_config}", "warning")
        else:
            console.say(f"{type(self)} do not have path")
        config |= class_config.basics
        super().__init__(game, config)

    def init_config(self):
        super().init_config()
        self.durability: float = self.config.durability
        self.position: str = self.config.position  # where to put the equipment
        self.additional_skill: list[Skill] = self.config.additional_skill


class Weapon:
    def __init__(self):
        if hasattr(self, "config") and hasattr(self, "game"):
            self.config |= self.game.config.item.weapon.basics
        else:
            console.say(f"Weapon without config/game", "error")

    def init_config(self):
        self.random_damages: bool = self.config.random_damages
        self.damages: int = self.config.damages
        self.min_damage: int = self.config.min_damages
        self.max_damage: int = self.config.max_damages
        self.heal: int = self.config.heal
        self.required_level: int = self.config.required_level
        self.target_type: str = self.config.target_type
        self.dodge: float = self.config.dodge
        self.critical_rate: float = self.config.critical_rate
        self.critical_damage_boost: float = self.config.critical_damage_boost
        self.effects: dict[FightStatus, float] = self.config._effects

    def useful(self, fight, character: FightingCharacter) -> bool:
        return any([self.useful_on(character) for character in fight.find_team(character, self.target_type)])

    def useful_on(self, character: FightingCharacter) -> bool:
        useful_attack = self.damages > 0 and character.health > 0
        useful_heal = self.heal > 0 and character.health < character.health.max
        useful_effects = len(self.effects) > 0
        return useful_attack | useful_heal | useful_effects

    def level_required(self, skill: FightSkill) -> bool:
        return skill.level >= self.required_level

    def find_target(self, fight, character: FightingCharacter) -> FightingCharacter:
        if self.game.io_mode == "console":
            target = console.request(
                "Select a target:",
                fight.player_team + fight.enemy_team,
                recommended_filter=lambda x: self.useful_on(x),
                valid_filter=lambda x: x in fight.find_team(character, self.target_type),
            )
            return target
        else:
            raise NotImplementedError

    def applied(self, fight, target: FightingCharacter, origin: FightingCharacter):
        console.say(f"{origin} used {self} on {target}")
        if self.damages > 0:
            fight.apply_damage_skill(self, target, origin)
        if self.heal > 0:
            fight.apply_heal_skill(self, target, origin)
        self.apply_effects(target)

    def apply_effects(self, target):
        for effect, probability in self.effects.items():
            if self.game.random_event(probability):
                target.get_fight_status(effect.with_config(self.game))


class Consumable(Item):
    def __init__(self, game, prev_config=None):
        class_config = default_config.item.consumable
        config = prev_config if prev_config is not None else MyDict()
        if hasattr(self, "path"):
            if self.path is not None:
                if self.path in class_config:
                    config |= class_config[self.path]
                    self.path = None
                else:
                    console.say(f"Should have {self.path} in {class_config}", "warning")
        else:
            console.say(f"{type(self)} do not have path")
        config |= class_config.basics
        super().__init__(game, config)

    def init_config(self):
        super().init_config()


class Potion(Consumable, Weapon):
    def __init__(self, game, prev_config=None):
        class_config = default_config.item.consumable.potion
        config = prev_config if prev_config is not None else MyDict()
        if hasattr(self, "path"):
            if self.path is not None:
                if self.path in class_config:
                    config |= class_config[self.path]
                    self.path = None
                else:
                    console.say(f"Should have {self.path} in {class_config}", "warning")
        else:
            console.say(f"{type(self)} do not have path", "warning")
        config |= class_config.basics
        super().__init__(game, config)

    def init_config(self):
        super().init_config()

    def consumed(self):
        pass
        # assert self.game.inventory[type(self)] > 0
        # self.game.inventory[type(self)] -= 1

    def applied(self, fight, target: FightingCharacter, origin: FightingCharacter):
        self.consumed()
        super().applied(fight, target, origin)




class Resource(Item):
    def __init__(self, game, prev_config=None):
        class_config = default_config.item.resource
        config = prev_config if prev_config is not None else MyDict()
        if hasattr(self, "path"):
            if self.path is not None:
                if self.path in class_config:
                    config |= class_config[self.path]
                    self.path = None
                else:
                    console.say(f"Should have {self.path} in {class_config}", "warning")
        else:
            console.say(f"{type(self)} do not have path")
        config |= class_config.basics
        super().__init__(game, config)

    def init_config(self):
        super().init_config()

        ###
        #####
        #######
        #########
        ###########
        #############
        ###############

    #################
    ###################
    #####################
    #######################





class FightStatus(Object, FightModifier):
    def __init__(self, game, prev_config=None):
        class_config = default_config.fight_status
        config = MyDict(prev_config if prev_config is not None else {})
        if hasattr(self, "path"):
            if self.path is not None:
                if self.path in class_config:
                    config |= class_config[self.path]
                    self.path = None
                else:
                    console.say(f"Should have {self.path} in {class_config}", "warning")
        else:
            console.say(f"{type(self)} do not have path")
        config |= class_config.basics
        super().__init__(game, config)

    def init_config(self):
        super().init_config()
        self.damages: int = self.config.damages
        self.heal: int = self.config.heal
        self.damages_rate = self.config.damages_rate
        self.console_color = self.config.console_color
        self.duration = self.config.duration

        ###

    #####
    #######
    #########
    ###########


class Status(Object):
    def __init__(self, game, prev_config=None):
        class_config = default_config.status
        config = MyDict(prev_config if prev_config is not None else {})
        if hasattr(self, "path"):
            if self.path is not None:
                if self.path in class_config:
                    config |= class_config[self.path]
                    self.path = None
                else:
                    console.say(f"Should have {self.path} in {class_config}", "warning")
        else:
            console.say(f"{type(self)} do not have path")
        config |= class_config.basics
        super().__init__(game, config)
