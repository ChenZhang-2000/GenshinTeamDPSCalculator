import json
import numpy as np

from common.stats import Stats, Buff, BasicBuff, ProportionalBuff


ENEMY_FACTORY = {}
ESTATS_LENGTH = 10


class EStats:
    length = ESTATS_LENGTH
    """
    0: hp
    1: 防御力
    2: 火元素抗性
    3: 水元素抗性
    4: 雷元素抗性
    5: 风元素抗性
    6: 冰元素抗性
    7: 岩元素抗性
    8: 物理抗性
    9: 草元素抗性
    """
    def __init__(self, array: np.array = np.zeros((1, ESTATS_LENGTH))):
        assert array.shape[1] == ESTATS_LENGTH
        self.data = array


def register_enemy(cls):
    cls_name = cls.__name__

    def register(cls):
        ENEMY_FACTORY[cls_name] = cls

    return register(cls)


class Enemy(object):
    def __init__(self):
        data = json.load(open(f"common\\enemy\\stats\\{self.__class__.__name__}.json"))

        self.stats = EStats(np.array(data['stats']).reshape(1, EStats.length))

