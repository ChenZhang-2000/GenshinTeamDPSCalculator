import numpy as np
import torch


STATS_LENGTH = 33
ESTATS_LENGTH = 12
SKILL_TYPE_MAP = {'a': 'a', 'A': 'A', 'e': 'e', 'E': 'e', 'q': 'q', 'Q': 'q',
                  'pl': 'l', 'PL_low': 'l', 'PL_high': 'l', 'p': 'o', 'P': 'o'}


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
        # print(1)
        return Stats(self.data + other)

    def __radd__(self, other):
        # print('-----------------------------------------------')
        # print(self.data)
        # print(other)
        return Stats(self.data + other)

    def __str__(self):
        return self.data.__str__()

    def copy(self):
        return Stats(torch.clone(self.data))

    def sum(self):
        self.data = np.sum(self.data, axis=0).reshape((1, STATS_LENGTH))


class Buff(Stats):
    def __init__(self, char, array: torch.tensor = torch.zeros(1, Stats.length),
                 skill_type = 'all', element_type='all'):
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
        self.element_type = element_type

    def valid(self, skill, team):
        return True

    def update(self, *args, **kwargs):
        pass


class BasicBuff(Buff):
    """
    This buff will bonus characters without condition
    """
    def __init__(self, char, array: torch.tensor = torch.zeros(1, Stats.length),
                 skill_type = 'all', element_type='all'):
        """
        char: index of the characters in the team
        array: numpy array of shape n x stats_length with each row being the values of the buff
        skill_type: type of buffed skill, accepted values: all, a, A, e=E, l=L, q=Q, p=P
        field_type: whether the buff will buff the characters on field only, accepted values: all, on, off
        element_type: whether the buff affect on certain elements, accepted values:
            all, pyro,  hydro, electro, anemo, cryo, geo, dendro, physical
        """
        # print(array)
        super().__init__(char, array, skill_type, )


class ProportionalBuff(Buff):
    """
    This buff will bonus characters without condition
    """
    def __init__(self, char, array: torch.tensor = torch.zeros(Stats.length, Stats.length),
                 skill_type = 'all', element_type='all'):
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
        super().__init__(char=char, skill_type=skill_type)

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
    def __init__(self, char, skill_infused: dict):
        """
        skill_type_from: the skill type to convert
        """
        self.char = char
        self.skill_type_from = skill_infused.keys()
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

    def __getitem__(self, idx):
        if isinstance(idx, str):
            if idx == 'pyro':
                return self.data[:, 2]
            elif idx == 'hydro':
                return self.data[:, 3]
            elif idx == 'electro':
                return self.data[:, 4]
            elif idx == 'cryo':
                return self.data[:, 5]
            elif idx == 'anemo':
                return self.data[:, 6]
            elif idx == 'geo':
                return self.data[:, 7]
            elif idx == 'dendro':
                return self.data[:, 8]
            elif idx == 'physical':
                return self.data[:, 9]
            else:
                raise KeyError
        else:
            return self.data.__getitem__(idx)

    def __add__(self, other):
        # print(1)
        return Monster(self.data + other)

    def __radd__(self, other):
        # print('-----------------------------------------------')
        # print(self.data)
        # print(other)
        return Monster(self.data + other)


class Debuff(Monster):
    def __init__(self, array: torch.tensor = torch.zeros(1, ESTATS_LENGTH)):
        super().__init__(array)

    def __add__(self, other):
        # print(1)
        return Debuff(self.data + other)

    def __radd__(self, other):
        # print('-----------------------------------------------')
        # print(self.data)
        # print(other)
        return Debuff(self.data + other)


class Skills:
    def __init__(self, char, scale, skill_type, element_type):
        self.char = char
        self.scale = scale
        self.skill_type = skill_type
        self.element_type = element_type
        self.reaction_factor = 1.

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
        elif self.element_type in buff.element_type:
            correct_element = True

        return correct_validation and correct_skill and correct_element

    def buff_skill(self, team, basic_buffs: {BasicBuff: {}}, proportion_buffs: {ProportionalBuff: {}}):
        """
        This method will check and update all the buffs of a skill, and changed the team stats to buffed stats


        Pseudo Code:

        """

        char = team[self.char.idx]

        for buff in char.weapon.permanent_buffs + char.artifact.permanent_buffs:
            if isinstance(buff, ProportionalBuff):
                proportion_buffs.append(buff)

        for buff in basic_buffs:
            if self.buff_valid(buff, team):
                team.add_basic_buff(buff, self.char.idx)

        for buff in proportion_buffs:
            if self.buff_valid(buff, team):
                team.add_basic_buff(buff, self.char.idx)

    def debuff_enemy(self, enemy, debuffs):
        for debuff in debuffs:
            enemy.change_stats(debuff)

    def damage(self, team, enemy, buffs: ([], [], []), reaction, infusion=None):
        """
        team: team object
        enemy: enemy object
        buffs: ([basic buffs], [proportional buffs], [debuffs])
        reaction: list of reactions
        infusion: infusion, default None

        Pseudo Code:

        if infusion != None do:
            return

        """
        reaction_factor = 1.
        if infusion:
            if self.char.idx == infusion.char.idx and self.skill_type in infusion.skill_types_from:
                return infusion.skills_infused[self.skill_type].dmage(team, enemy, buffs, reaction)
        else:
            self.buff_skill(team, buffs[0], buffs[1])
            self.debuff_enemy(enemy, buffs[2])
            c_idx = self.char.idx
            stats = team[c_idx]
            dmg = self.calculate(stats, enemy)
            team.init_stats()
            enemy.init_stats()
            return dmg * reaction_factor

    def calculate(self, stats, enemy):
        """
        stats:
        """
        scale = self.scale
        atk = stats[0] * (1 + stats[2]/100) + stats[1]
        additional = stats[32]
        critical = 1 + (stats[9] * stats[10] / 10000)
        dmg_bonus = 1 + (stats[self.element_type] / 100) + (stats[31] / 100)
        resistance = enemy[self.element_type]
        if resistance < 0:
            resistance = 1 - resistance/200
        elif resistance > 75:
            resistance = 1 / (1 + 4 * resistance/100)
        else:
            resistance = 1 - resistance/100
        defence = enemy[1] * (1 - enemy[11] / 100)

        return damage(scale, atk, additional, critical, dmg_bonus, resistance, defence)


class PolySkills:
    def __init__(self, char, scales, skill_type, element_type):
        self.char = char
        self.strike_length = len(scales)
        self.skills = [Skills(char, scale, skill_type, element_type) for scale in scales]
        self.skill_type = skill_type
        self.element_type = element_type

    def damage(self, team, enemy, buffs: ([], [], []), reaction, infusion=None, strike=1):
        dmg = 0
        if infusion:
            if self.char.idx == infusion.char.idx and self.skill_type in infusion.skill_types_from:
                return infusion.skills_infused[self.skill_type].dmage(team, enemy, buffs, reaction, strike)
        else:
            for i in range(strike):
                dmg += self.skills[i % self.strike_length].damage(team, enemy, buffs, reaction, infusion)
            return dmg


class TransformativeReaction(Reaction, Skills):
    pass


def damage(scale, atk, additional, critical, dmg_bonus, resistance, defence):
    return (scale * atk + additional) * critical * dmg_bonus * resistance * defence

