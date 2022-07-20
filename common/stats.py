import numpy as np
import torch


STATS_LENGTH = 33
ESTATS_LENGTH = 12
SKILL_TYPE_MAP = {'a': 'a', 'A': 'A', 'e': 'e', 'E': 'e', 'q': 'q', 'Q': 'q', 'l': 'l', 'L': 'l'}


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

    27：草元素伤害加成
    28：草元素抗性

    29：物理伤害加成
    30：物理抗性

    31：其他增伤
    
    32：附加伤害
    """
    def __init__(self, array: torch.tensor = torch.zeros(1, STATS_LENGTH)):
        assert array.shape[1] == STATS_LENGTH, f"{array.shape[1]} {STATS_LENGTH}"
        self.data = array

    def __getitem__(self, idx):
        if isinstance(idx, str):
            if idx == 'pyro':
                return self.data[:, 15]
            elif idx == 'hydro':
                return self.data[:, 17]
            elif idx == 'electro':
                return self.data[:, 19]
            elif idx == 'cryo':
                return self.data[:, 21]
            elif idx == 'anemo':
                return self.data[:, 23]
            elif idx == 'geo':
                return self.data[:, 25]
            elif idx == 'dendro':
                return self.data[:, 27]
            elif idx == 'physical':
                return self.data[:, 29]
            else:
                raise KeyError
        else:
            return self.data.__getitem__(idx)

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
        return Stats(torch.clone(self.data))

    def sum(self):
        self.data = np.sum(self.data, axis=0).reshape((1, STATS_LENGTH))


class Buff(Stats):
    def __init__(self, char, array: torch.tensor = torch.zeros(1, Stats.length),
                 skill_type: str = 'all', field_type: str = 'all', element_type='all'):
        """
        char: index of the characters in the team
        array: numpy array of shape n x stats_length with each row being the values of the buff
        skill_type: type of buffed skill, accepted values: all, a, A, e=E, l=L, q=Q, p=P
        field_type: whether the buff will buff the characters on field only, accepted values: all, on, off
        element_type: whether the buff affect on certain elements, accepted values:
            all, pyro,  hydro, electro, anemo, cryo, geo, physical
        """
        # print(array)
        self.char = char
        super().__init__(array)
        self.skill_type = skill_type
        self.field_type = field_type
        self.element_type = element_type

    def valid(self, skill, team):
        return True


class BasicBuff(Buff):
    """
    This buff will bonus characters without condition
    """
    def __init__(self, char, array: torch.tensor = torch.zeros(1, Stats.length),
                 skill_type: str = 'all', field_type: str = 'all', element_type='all'):
        """
        char: index of the characters in the team
        array: numpy array of shape n x stats_length with each row being the values of the buff
        skill_type: type of buffed skill, accepted values: all, a, A, e=E, l=L, q=Q, p=P
        field_type: whether the buff will buff the characters on field only, accepted values: all, on, off
        element_type: whether the buff affect on certain elements, accepted values:
            all, pyro,  hydro, electro, anemo, cryo, geo, dendro, physical
        """
        # print(array)
        super().__init__(char, array, skill_type, field_type)


class ProportionalBuff(Buff):
    """
    This buff will bonus characters without condition
    """
    def __init__(self, char, array: torch.tensor = torch.zeros(Stats.length, Stats.length),
                 skill_type: str = 'all', field_type: str = 'all', element_type='all'):
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
        self.func = lambda x:  array @ x
        super().__init__(char=char, skill_type=skill_type, field_type=field_type)

    def load_buff(self, stats):
        """
        This function will calculate the buffed values based on the team stats.

        stats: numpy array of team stats with shape 4 x stats_length
        """
        stats = torch.clone(stats[self.char])
        stats[:, [1, 4, 7]] += (1 + stats[:, [2, 5, 8]] / 100) * stats[:, [0, 3, 6]]
        stats[:, [2, 5, 8]] = 0
        self.data = self.func(stats)


class Infusion:
    def __init__(self, char, skill_type_from, skill_infused):
        """
        skill_type_from: the skill type to convert
        """
        self.char = char
        self.skill_type_from = skill_type_from
        self.skill_infused = skill_infused


class Reaction:
    pass


class AmplifyingReaction(Reaction):
    pass


class Monster:
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
    8: 草元素抗性
    9: 物理抗性
    10: 防御力固定值削减
    11: 防御力百分比削减
    """
    def __init__(self, array: torch.tensor = torch.zeros(1, ESTATS_LENGTH)):
        assert array.shape[1] == ESTATS_LENGTH
        # print(array)
        self.data = array
        self.hp = array[0, 0]
        self.defence = array[0, 1]
        self.res = array[0, 2:]


class Debuff(Monster):
    pass


class Skills:
    def __init__(self, char, scale, skill_type, element_type):
        self.char = char
        self.scale = scale
        self.skill_type = skill_type
        self.element_type = element_type

    def buff_valid(self, buff, team):
        correct_skill = False
        correct_validation = False
        correct_element = False

        if buff.skill_type == 'all':
            correct_skill = True
        elif buff.skill_type == self.skill_type:
            correct_skill = True

        if buff.valid(self, team):
            correct_validation = True

        if buff.element_type == 'all':
            correct_element = True
        elif buff.element_type == self.element_type:
            correct_element = True

        return correct_validation and correct_skill and correct_element

    def buff_skill(self, team, buffs):
        """
        This decorator will check all the buffs of a skill, and changed the team stats to buffed stats


        Pseudo Code:

        """

        char = team[self.char.idx]

        basic_buffs = []
        proportion_buffs = []

        for b in char.weapon.permanent_buffs + char.artifact.permanent_buffs:
            if isinstance(b, BasicBuff):
                char.stats.data += b
            elif isinstance(b, ProportionalBuff):
                proportion_buffs.append(b)

        for buff in buffs:
            if isinstance(buff, BasicBuff):
                basic_buffs.append(buff)
            elif isinstance(buff, ProportionalBuff):
                proportion_buffs.append(buff)

        for b in basic_buffs:
            if self.buff_valid(b, team):
                team.add_basic_buff(b, self.char.idx)

        for b in proportion_buffs:
            if self.buff_valid(b, team):
                team.add_basic_buff(b, self.char.idx)

    def debuff_enemy(self, enemy):
        pass

    def damage(self, team, enemy, buffs, reaction, infusion=None):
        """


        Pseudo Code:

        if infusion != None do:
            return

        """
        if infusion:
            if self.char.idx == infusion.char.idx and infusion.skill_type_from == self.skill_type:
                return infusion.skill_infused.dmage(team, enemy, buffs, reaction)
        else:
            self.buff_skill(team, buffs)
            self.debuff_enemy(enemy, )
            c_idx = self.char.idx
            stats = team[c_idx]
            self.calculate(stats, enemy)

    def calculate(self, stats, enemy):
        """
        stats:
        """


class TransformativeReaction(Reaction, Skills):
    pass


def damage(scale, atk, additional, critical, dmg_bonus, resistance, defence):
    return (scale * atk + additional) * critical * dmg_bonus * resistance * defence

