import toml
import collections.abc
import random
from collections import UserDict
from collections.abc import Iterable

import skills
import character
import status
import place
import item



class MyDict(UserDict):

    game = None
    debug = False
    small_debug = False
    @classmethod
    def get_default(cls):
        with open("config.toml", "r") as config_file:
            config = toml.load(config_file)
        return cls.add_complement(config)

    @classmethod
    def add_complement(cls, config):
        return cls(config)

    def transform(self, data):
        if self.game is not None:
            if self.debug or self.small_debug:
                print("Looks like a game is Known")
            if isinstance(data, str):
                if data[0] == "*":
                    new_data = data[1:]
                    if self.debug:
                        print("I am transforming", new_data)
                    if new_data in self.game.__dict__:
                        return getattr(self.game, new_data)
                    else:
                        if self.debug:
                            print("Not in game :", self.game.__dict__)
                    for lib in self.game.libs:
                        if new_data in lib.__dict__:
                            return getattr(lib, new_data)
                    raise ValueError(f"Lib not found for {new_data}")
                else:
                    return data
            elif isinstance(data, Iterable):
                if self.debug:
                    print("I am propaging Transformation through", data)
                if isinstance(data, dict):
                    return MyDict(map(self.transform, data.items()))
                return type(data)(map(self.transform, data))
            else:
                return data
        else:
            if self.debug or self.small_debug:
                print(f"Pas de Game renseignée, je ne transforme pas")
            return data


    def get_val(self, name):
        if "mini_" + name in self.data and "maxi_" + name in self.data:
            return random.uniform(self.data["mini_" + name], self.data["maxi_" + name])
        elif name in self.data:
            return self.transform(self.data[name])
        else:
            raise AttributeError(name)

    def __getattr__(self, attr):
        if attr[0] == "_":
            return self.get_val(attr[1:])
        if attr in self.data and isinstance(self.data[attr], collections.abc.Mapping):
            return MyDict(**self.data[attr])
        return self.get_val(attr)

    # def __repr__(self):
    #     return "MyDict " + super(MyDict, self).__repr__()




default_config = MyDict.get_default()
