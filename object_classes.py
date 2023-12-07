import console
from boundedValue import BoundedValue
from config import MyDict, default_config


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

    def init_config(self):
        if not self.config_initialized:
            self.non_init_instances.remove(self)
            self.config_initialized = True
        else:
            print(f"{self.name} got initalized again")

    def __repr__(self):
        return self.name

    @classmethod
    def with_config(cls, game):
        obj = cls(game)
        obj.game.init_config_all()
        return obj


class InitClass:

    def __init__(self):
        pass


        ###
       #####
      #######
     #########
    ###########
   #############
  ###############
 #################
###################
### S K I L L S ###
###################
 #################
  ###############
   #############
    ###########
     #########
      #######
       #####
        ###


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
        self.action_consumption: int = self.config.action_consumption
        self.cooldown: int = self.config.cooldown
        self.mono_target = True
        self.target_type: str = self.config.target_type  # self, enemy, ally, all
        self.target_number: int = self.config.target_number  # [1, +inf]
        self.damages: int = self.config.damages
        self.critical_rate: float = self.config.critical_rate
        self.dodge: float = self.config.dodge

    def applied(self, fight, target, origin, *args):
        fight.apply_damage_skill(self, target, origin)

    def train(self):
        super().train()
        self.damages *= 1.5

    def fight_selected(self, fight, character) -> list:
        return []

    def request_target(self, fight, character, *add_args):
        return fight.request_target(self, character)


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
 #########################
###########################
### C H A R A C T E R S ###
###########################
 #########################
  #######################
   #####################
    ###################
     #################
      ###############
       #############
        ###########
         #########
          #######
           #####
            ###

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

    def say(self, what, bold=True, end="\n", map_what=True):
        console.say(what, self, bold, end, map_what)

    def add_status(self, status):
        console.say(f"{self.name} is now {status}", "warning")


class FightingCharacter(Character):

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
        self.critical_rate_boost: float = self.config.critical_rate_boost
        self.critical_rate_drop: float = self.config.critical_rate_drop
        self.damage_boost: float = self.config.damage_boost
        self.defense_boost: float = self.config.defense_boost
        self.precision_boost: float = self.config.precision_boost
        self.dodge_boost: float = self.config.dodge_boost
        self.critical_defense_boost:float = self.config.critical_defense_boost

        self.equipments: list = self.config.equipments

    def get_damage(self, damages):
        self.health -= damages
        # print(f"{self} has {self.health.str_max()} points of life")

    def compute_boost(self, attr, skill):
        new_attr = attr + "_boost"
        return (getattr(self, new_attr) *
                self.game.list_product([getattr(fs, new_attr) for fs in self.fight_statuses]) *
                self.game.list_product([getattr(equip, new_attr) for equip in self.equipments]) *
                self.game.list_product([getattr(status, new_attr) for status in self.fight_statuses]))
        # Could add boost linked to skill

    def compute_drop(self, attr, skill):
        new_attr = attr + "_drop"
        return (getattr(self, new_attr) *
                self.game.list_product([getattr(fs, new_attr) for fs in self.fight_statuses]) *
                self.game.list_product([getattr(equip, new_attr) for equip in self.equipments]) *
                self.game.list_product([getattr(status, new_attr) for status in self.fight_statuses]))
        # Could add drop linked to skill

    def fight_statuses_update(self):
        for status in self.fight_statuses:
            if status.duration == 0:
                self.fight_statuses.remove(status)
            status.duration -= 1
        for new_status in self.new_fight_statuses:
            self.get_fight_status(new_status)
        self.new_fight_statuses = []

    def get_fight_status_delayed(self, status):
        self.new_fight_statuses.append(status)

    def get_fight_status(self, new_status):
        console.say(f"{self} is now {new_status} for {new_status.duration}")
        self.fight_statuses.append(new_status)

    def attack_stop(self):
        for status in self.fight_statuses:
            if status.attack_stop:
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
   ###########
  #############
 ###############
#################
### I T E M S ###
#################
 ###############
  #############
   ###########
    #########
     #######
      #####
       ###
        #

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

    def init_config(self):
        super().init_config()
        self.name: str = self.config.name
        self.rarity: int = self.config.rarity
        self.description: str = self.config.description

        if isinstance(self, Craftable):
            Craftable.init_config(self)


class Craftable:

    def __init__(self):
        self.config |= self.game.config.item.craftable.basics

    def init_config(self):
        self.known: bool = self.config.known
        self.recipe: dict[Item, int] = self.config._recipe


class Equipment(Item):

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


class Weapon(Equipment):

    def __init__(self, game, prev_config=None):
        class_config = default_config.item.equipment.weapon
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
        self.min_damage: int = self.config.min_damage
        self.max_damage: int = self.config.max_damage
        self.effects: list[Skill] = self.config.effects


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
        self.effects: list[Status] = self.config.effects


class Potion(Consumable):

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
            console.say(f"{type(self)} do not have path")
        config |= class_config.basics
        super().__init__(game, config)

    def init_config(self):
        super().init_config()
        self.required_level = self.config.required_level
        self.target = self.config.target
        self.damage = self.config.damage

    def useful(self, fight, character: FightingCharacter) -> bool:
        return True

    def useful_on(self, character: FightingCharacter) -> bool:
        return True

    def level_required(self, character: FightingCharacter) -> bool:
        from skills import PotionThrow

        max_level = 0
        for skill in character.fight_skill:
            if type(skill) is PotionThrow:
                max_level = max(max_level, skill.level)
        return max_level >= self.required_level

    def find_target(self, fight, character: FightingCharacter) -> FightingCharacter:
        if self.game.io_mode == "console":
            target = console.request("Select a target:",
                                     fight.player_team + fight.enemy_team,
                                     recommended_filter=lambda x: self.useful_on(x),
                                     valid_filter=lambda x: x in (fight.enemy_team if (character in fight.player_team) ^ (self.target == "ally") else fight.player_team))
            return target
        else:
            raise NotImplementedError

    def applied(self, character: FightingCharacter):
        character.get_damage(self.damage)
        for effect in self.effects:
            character.add_status(effect)





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
   #########################
  ###########################
 #############################
###############################
### F I G H T   S T A T U S ###
###############################
 #############################
  ###########################
   #########################
    #######################
     #####################
      ###################
       #################
        ###############
         #############
          ###########
           #########
            #######
             #####
              ###


class FightStatus(Object):

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
        self.duration = self.config.duration
        self.precision_boost = self.config.precision_boost
        self.damage_boost = self.config.damage_boost
        self.defense_boost = self.config.defense_boost
        self.health_boost = self.config.health_boost
        self.health_drop = self.config.health_drop
        self.critical_damage_boost = self.config.critical_damage_boost
        self.critical_defense_boost = self.config.critical_defense_boost
        self.critical_rate_boost = self.config.critical_rate_boost
        self.critical_rate_drop = self.config.critical_rate_drop



        ###
       #####
      #######
     #########
    ###########
   #############
  ###############
 #################
###################
### S T A T U S ###
###################
 #################
  ###############
   #############
    ###########
     #########
      #######
       #####
        ###

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
