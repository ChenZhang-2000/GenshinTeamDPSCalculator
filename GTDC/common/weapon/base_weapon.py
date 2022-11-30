import json
import os

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
        file_name = os.path.join(os.path.dirname(__file__), f'stats\\{self.__class__.__name__}.json')
        data = json.load(open(file_name))

        self.stats = Stats(torch.tensor(data['stats']).reshape(1, Stats.length))
        self.permanent_buffs = []
        self.buffs = []

    def init_char(self, char):
        self.char = char
