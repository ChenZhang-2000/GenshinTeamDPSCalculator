import json
import numpy as np

from common.stats import Stats, Buff, BasicBuff, ProportionalBuff


CHAR_FACTORY = {}
SKILL_TYPE_MAP = {'a': 'a', 'A': 'A', 'e': 'e', 'E': 'e', 'q': 'q', 'Q': 'q', 'l': 'l', 'L': 'l'}


def register_char(cls):
    cls_name = cls.__name__

    def register(cls):
        CHAR_FACTORY[cls_name] = cls

    return register(cls)


def add_buff(buff, stats, types):
    buff.sum()
    correct_skill = False
    correct_field = False
    correct_element = False

    if buff.skill_type == 'all':
        correct_skill = True
    elif buff.skill_type == types[0]:
        correct_skill = True

    if buff.field_type == 'all':
        correct_field = True

    elif buff.field_type == 'on' and types[1]:
        correct_field = True

    elif buff.field_type == 'off' and not types[1]:
        correct_field = True

    if buff.element_type == 'all':
        correct_element = True

    elif buff.element_type == types[2]:
        correct_element = True

    if correct_field and correct_skill and correct_element:
        stats[buff.char_idx] += buff.data


def buff(func):
    """
    This decorator will check all the buffs of a skill, and changed the team stats to buffed stats
    """
    name = func.__name__

    def buff_func(self, *args, **kwargs):
        nonlocal name
        func_types = [SKILL_TYPE_MAP[name[-1]], self.on_field == self.idx, kwargs['element']]
        # [skill_type, field_type, element_type]
        basic_buffs = []
        proportion_buffs = []
        stats = self.team_stats.copy()

        for buff in self.weapon.permanent_buffs + self.artifact.permanent_buffs:
            if isinstance(buff, BasicBuff):
                self.stats.data += buff
            elif isinstance(buff, ProportionalBuff):
                proportion_buffs.append(buff)

        for arg in args:
            if isinstance(arg, BasicBuff):
                basic_buffs.append(arg)
            elif isinstance(arg, ProportionalBuff):
                proportion_buffs.append(arg)

        for buff in basic_buffs:
            add_buff(buff, stats, func_types)

        before_prop = stats.copy()
        for buff in proportion_buffs:
            buff.load_buff(before_prop)
            add_buff(buff, stats, func_types)

        self.set_team_stats(stats)
        return func(self, *args, **kwargs)

    return buff_func


class Character(object):
    def __init__(self, weapon, enemy, artifact):
        data = json.load(open(f"common\\characters\\stats\\{self.__class__.__name__}.json"))

        self.idx = 0
        self.element = data['element']

        # print(np.array(data['stats']).reshape(1, Stats.length))
        # print(weapon.stats.data)
        # print(np.array(data['stats']).reshape(1, Stats.length) + weapon.stats.data)
        self.stats = Stats(np.array(data['stats']).reshape(1, Stats.length) + weapon.stats.data + artifact.stats.data)
        self.team_stats = Stats(np.zeros((4, Stats.length)))
        self.scaling = data['skills']
        self.on_field = 0

        self.weapon = weapon
        self.enemy = enemy
        self.artifact = artifact

        self.buff_a = Stats()
        self.buff_A = Stats()
        self.buff_e = Stats()
        self.buff_E = Stats()
        self.buff_q = Stats()
        self.buff_Q = Stats()
        self.buff_p = Stats()
        self.buff_P = Stats()

    def set_idx(self, idx):
        self.idx = idx
        self.weapon.set_char_idx(idx)
        self.artifact.set_char_idx(idx)

    def set_team_stats(self, stats):
        self.team_stats = stats
        self.stats = Stats(self.team_stats[self.idx].reshape(1, Stats.length))

    def set_on_field(self, on_field):
        self.on_field = on_field

    @buff
    def skill_a(self, counter, element, buff=None):
        scaling = self.stats['skills']['a']
        return self.element, scaling[counter, 0].reshape(1, 1), self.stats

    @buff
    def skill_A(self, element, buff=None):
        scaling = self.stats['skills']['A']
        return self.element, scaling[:, 0].reshape(scaling.shape[0], 1), self.stats

    @buff
    def skill_l(self, element, buff=None):
        scaling = self.stats['skills']['pl']
        return self.element, scaling[0, 0].reshape(1, 1), self.stats

    @buff
    def skill_L(self, element, buff=None):
        scaling = self.stats['skills']['PL']
        return self.element, scaling[1, 0].reshape(1, 1), self.stats

    @buff
    def skill_e(self, element, buff=None):
        scaling = self.stats['skills']['e']
        return self.element, scaling[0, 0].reshape(1, 1), self.stats

    @buff
    def skill_E(self, element, buff=None):
        scaling = self.stats['skills']['E']
        return self.element, scaling[0, 0].reshape(1, 1), self.stats

    @buff
    def skill_q(self, element, buff=None):
        scaling = self.stats['skills']['q']
        return self.element, scaling[0, 0].reshape(1, 1), self.stats

    @buff
    def skill_Q(self, element, buff=None):
        scaling = self.stats['skills']['Q']
        return self.element, scaling[0, 0].reshape(1, 1), self.stats

    @buff
    def skill_p(self, element, buff=None):
        scaling = self.stats['skills']['p']
        return self.element, scaling[0, 0].reshape(1, 1), self.stats

    @buff
    def skill_P(self, element, buff=None):
        scaling = self.stats['skills']['P']
        return self.element, scaling[0, 0].reshape(1, 1), self.stats


if __name__ == "__main__":
    @register_char
    class RaidenShogun(Character):
        def __init__(self, weapon, enemy):
            super().__init__(weapon, enemy)

    # char = RaidenShogun()
    pass
