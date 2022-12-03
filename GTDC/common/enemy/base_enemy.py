import json
import os

import torch

from GTDC.common.stats import Stats, Buff, BasicBuff, ProportionalBuff, ESTATS_LENGTH, Monster


ENEMY_FACTORY = {}


def register_enemy(cls):
    cls_name = cls.__name__

    def register(cls):
        ENEMY_FACTORY[cls_name] = cls

    return register(cls)


class Enemy(Monster):
    def __init__(self, level):
        file_name = os.path.join(os.path.dirname(__file__), f'stats\\{self.__class__.__name__}.json')
        data = json.load(open(file_name))
        super().__init__(array=torch.tensor(data['stats']).reshape(1, Monster.length))
        self.stats = self.data - 0
        self.dynamic_stats = self.data - 0
        self.level = level

    def __getitem__(self, idx):
        if isinstance(idx, str):
            if idx == 'pyro':
                return self.stats[:, 2]
            elif idx == 'hydro':
                return self.stats[:, 3]
            elif idx == 'electro':
                return self.stats[:, 4]
            elif idx == 'cryo':
                return self.stats[:, 5]
            elif idx == 'anemo':
                return self.stats[:, 6]
            elif idx == 'geo':
                return self.stats[:, 7]
            elif idx == 'dendro':
                return self.stats[:, 8]
            elif idx == 'physical':
                return self.stats[:, 9]
            else:
                raise KeyError
        else:
            return self.data[idx]

    def change_stats(self, residual):
        self.dynamic_stats = self.stats + residual

    def init_stats(self):
        self.dynamic_stats = self.stats + 0


