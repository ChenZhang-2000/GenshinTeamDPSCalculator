import json
import numpy as np

from common.stats import Stats, Buff, BasicBuff, ProportionalBuff


WEAPON_FACTORY = {}


def register_weapon(cls):
    cls_name = cls.__name__

    def register(cls):
        WEAPON_FACTORY[cls_name] = cls

    return register(cls)


class Weapon(object):
    def __init__(self):
        data = json.load(open(f"common\\weapon\\stats\\{self.__class__.__name__}.json"))

        self.char_idx = 0
        self.stats = Stats(np.array(data['stats']).reshape(1, Stats.length))
        self.permanent_buffs = []
        self.partial_buffs = []

    def set_char_idx(self, idx):
        self.char_idx = idx
