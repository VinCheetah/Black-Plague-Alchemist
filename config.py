import toml
import collections.abc
import random
from collections import UserDict


class Config(UserDict):

    @classmethod
    def get_default(cls):
        with open("config.toml", "r") as config_file:
            config = toml.load(config_file)
        return cls.add_complement(config)

    @classmethod
    def add_complement(cls, config):
        return cls(config)

    def get_val(self, name):
        if "mini_" + name in self.data and "maxi_" + name in self.data:
            return random.uniform(self.data["mini_" + name], self.data["maxi_" + name])
        elif name in self.data:
            return self.data[name]
        else:
            raise AttributeError(name)

    def __getattr__(self, attr):
        if attr in self.data and isinstance(self.data[attr], collections.abc.Mapping):
            return Config(**self.data[attr])
        return self.get_val(attr)

    def __repr__(self):
        return "Config " + super(Config, self).__repr__()


default_config = Config.get_default()