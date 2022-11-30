import json
import torch

from GTDC.common.stats import Stats, Buff, BasicBuff, ProportionalBuff


WEAPON_FACTORY = {}


def register_weapon(cls):
    cls_name = cls.__name__

    def register(cls):
        WEAPON_FACTORY[cls_name] = cls

    return register(cls)


class Weapon(object):
    def __init__(self, affix=1):
        data = json.load(open(f"common\\weapon\\stats\\{self.__class__.__name__}.json"))

        self.stats = Stats(torch.tensor(data['stats']).reshape(1, Stats.length))
        self.permanent_buffs = []
        self.buffs = []

    def init_char(self, char):
        self.char = char
