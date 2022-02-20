import numpy as np


STATS_LENGTH = 30


class Stats:
    length = STATS_LENGTH
    """
    0：基础攻击力
    1：固定攻击力加成
    2：百分比攻击力加成

    3：基础防御力
    4：固定防御力加成
    5：百分比防御力加成

    6：基础生命值
    7：固定生命值加成
    8：百分比生命值加成

    9：元素精通
    10：暴击率
    11：暴击伤害
    12：治疗加成
    13：元素充能效率
    14：护盾强效

    15：火元素伤害加成
    16：火元素抗性

    17：水元素伤害加成
    18：水元素抗性

    19：雷元素伤害加成
    20：雷元素抗性

    21：风元素伤害加成
    22：风元素抗性

    23：冰元素伤害加成
    24：冰元素抗性

    25：岩元素伤害加成
    26：岩元素抗性

    27：物理伤害加成
    28：物理抗性

    29：附加伤害
    """
    def __init__(self, array: np.array = np.zeros((1, STATS_LENGTH))):
        assert array.shape[1] == STATS_LENGTH
        self.data = array

    def __getitem__(self, idx):
        return self.data[idx]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __add__(self, other):
        print(1)
        return self.data + other

    def __radd__(self, other):
        print('-----------------------------------------------')
        print(self.data)
        print(other)
        return self.data + other

    def __sub__(self, other):
        return self.data - other

    def __rsub__(self, other):
        return other - self.data

    def __mul__(self, other):
        return self.data * other

    def __rmul__(self, other):
        return other * self.data

    def __floordiv__(self, other):
        return self.data // other

    def __rfloordiv__(self, other):
        return other // self.data

    def __truediv__(self, other):
        return self.data / other

    def __rtruediv__(self, other):
        return other / self.data

    def __pow__(self, other):
        return self.data ** other

    def __rpow__(self, other):
        return other ** self.data

    def __str__(self):
        return self.data.__str__()

    def copy(self):
        return Stats(np.copy(self.data))

    def sum(self):
        self.data = np.sum(self.data, axis=0).reshape((1, STATS_LENGTH))


class Buff(Stats):
    def __init__(self, char: int, array: np.array = np.zeros((1, Stats.length)),
                 skill_type: str = 'all', field_type: str = 'all', element_type = 'all'):
        """
        char: index of the characters in the team
        array: numpy array of shape n x stats_length with each row being the values of the buff
        skill_type: type of buffed skill, accepted values: all, a, A, e=E, l=L, q=Q, p=P
        field_type: whether the buff will buff the characters on field only, accepted values: all, on, off
        element_type: whether the buff affect on certain elements, accepted values:
            all, pyro,  hydro, electro, anemo, cryo, geo, physical
        """
        # print(array)
        super().__init__(array)
        self.char_idx = char
        self.skill_type = skill_type
        self.field_type = field_type
        self.element_type = element_type


class BasicBuff(Buff):
    """
    This buff will bonus characters without condition
    """
    def __init__(self, char: int, array: np.array = np.zeros((1, Stats.length)),
                 skill_type: str = 'all', field_type: str = 'all', element_type = 'all'):
        """
        char: index of the characters in the team
        array: numpy array of shape n x stats_length with each row being the values of the buff
        skill_type: type of buffed skill, accepted values: all, a, A, e=E, l=L, q=Q, p=P
        field_type: whether the buff will buff the characters on field only, accepted values: all, on, off
        element_type: whether the buff affect on certain elements, accepted values:
            all, pyro,  hydro, electro, anemo, cryo, geo, physical
        """
        # print(array)
        super().__init__(char, array, skill_type, field_type)


class ProportionalBuff(Buff):
    """
    This buff will bonus characters without condition
    """
    def __init__(self, char: int, array: np.array = np.zeros((2, Stats.length)),
                 skill_type: str = 'all', field_type: str = 'all', element_type = 'all'):
        """
        char: index of the characters in the team
        array: numpy array of shape 2 x stats_length with first row being the proportions, the second row being the one hot
            index for the stats to be buffed.
        skill_type: type of buffed skill, accepted values: all, a, A, e=E, l=L, q=Q, p=P
        field_type: whether the buff will buff the characters on field only, accepted values: all, on, off
        element_type: whether the buff affect on certain elements, accepted values:
            all, pyro,  hydro, electro, anemo, cryo, geo, physical
        """
        # print(array)
        assert array.shape == (2, Stats.length)
        self.func = lambda x: x @ array[0] * array[1]
        super().__init__(char=char, skill_type=skill_type, field_type=field_type)

    def load_buff(self, stats):
        """
        This function will calculate the buffed values based on the team stats.

        stats: numpy array of team stats with shape 4 x stats_length
        """
        stats = np.copy(stats[self.char_idx])
        stats[:, [1, 4, 7]] = stats[:, [1, 4, 7]] * stats[:, [0, 3, 6]] / 100
        self.data = self.func(stats)

