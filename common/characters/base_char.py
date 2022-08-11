import json
import numpy as np
import torch

from common.stats import Stats, Buff, BasicBuff, ProportionalBuff, Skills, PolySkills, SKILL_TYPE_MAP


CHAR_FACTORY = {}


def register_char(cls):
    cls_name = cls.__name__

    def register(cls):
        CHAR_FACTORY[cls_name] = cls

    return register(cls)


# def add_buff(buff, stats, types):
#     buff.sum()
#     correct_skill = False
#     correct_field = False
#     correct_element = False
#
#     if buff.skill_type == 'all':
#         correct_skill = True
#     elif buff.skill_type == types[0]:
#         correct_skill = True
#
#     if buff.field_type == 'all':
#         correct_field = True
#     elif buff.field_type == 'on' and types[1]:
#         correct_field = True
#     elif buff.field_type == 'off' and not types[1]:
#         correct_field = True
#
#     if buff.element_type == 'all':
#         correct_element = True
#     elif buff.element_type == types[2]:
#         correct_element = True
#
#     if correct_field and correct_skill and correct_element:
#         stats[buff.char_idx] += buff.data


# def buff_skill(func):
#     """
#     This decorator will check all the buffs of a skill, and changed the team stats to buffed stats
#     """
#     name = func.__name__
#
#     def buff_func(self, *args, **kwargs):
#         nonlocal name
#         func_types = [SKILL_TYPE_MAP[name[-1]],
#                       self.on_field == self.idx,
#                       kwargs['element']]
#         # [skill_type, field_type, element_type]
#         basic_buffs = []
#         proportion_buffs = []
#         stats = self._team_stats.copy()
#
#         for b in self.weapon.permanent_buffs + self.artifact.permanent_buffs:
#             if isinstance(b, BasicBuff):
#                 self.stats.data += b
#             elif isinstance(b, ProportionalBuff):
#                 proportion_buffs.append(b)
#
#         for arg in args+kwargs['buff']:
#             if isinstance(arg, BasicBuff):
#                 basic_buffs.append(arg)
#             elif isinstance(arg, ProportionalBuff):
#                 proportion_buffs.append(arg)
#
#         for b in basic_buffs:
#             add_buff(b, stats, func_types)
#
#         before_prop = stats.copy()
#         for buff in proportion_buffs:
#             buff.load_buff(before_prop)
#             add_buff(buff, stats, func_types)
#
#         self.set_team_stats(stats)
#
#         return func(self, *args, **kwargs)
#
#     return buff_func


class Character(object):
    def __init__(self, weapon, artifact, level=90, constellation=0):
        data = json.load(open(f"common\\characters\\stats\\{self.__class__.__name__}.json"))

        self.idx = 0
        self.element = data['element']
        self.level = level
        self.constellation = constellation

        # print(type(torch.tensor(data['stats']).reshape(1, Stats.length)))
        # print(type(weapon.stats.data))
        # print(type(artifact.stats))
        self.stats = Stats(torch.tensor(data['stats']).reshape(1, Stats.length) + weapon.stats.data + artifact.stats.data)
        # self._team_stats = Stats(torch.zeros(4, Stats.length))
        # self.team_stats = Stats(torch.zeros(4, Stats.length))
        self.scaling = data['skills']
        # self.on_field = 0

        self.weapon = weapon
        self.artifact = artifact

        self.skill_a = PolySkills(self, [sum(i) for i in self.scaling['a']], 'a', 'physical')
        self.skill_A = Skills(self, sum(self.scaling['A']), 'A', 'physical')
        self.skill_pl = Skills(self, sum(self.scaling['pl']), 'pl', 'physical')
        self.skill_PL_low = Skills(self, self.scaling['PL'][0], 'PL_low', 'physical')
        self.skill_PL_high = Skills(self, self.scaling['PL'][1], 'PL_high', 'physical')
        self.skill_e = Skills(self, sum(self.scaling['e']), 'e', self.element)
        self.skill_E = Skills(self, sum(self.scaling['E']), 'E', self.element)
        self.skill_q = Skills(self, sum(self.scaling['q']), 'q', self.element)
        self.skill_Q = Skills(self, sum(self.scaling['Q']), 'Q', self.element)
        self.skill_p = Skills(self, sum(self.scaling['p']), 'p', self.element)
        self.skill_P = Skills(self, sum(self.scaling['P']), 'P', self.element)

        self.skills = {"a": self.skill_a,
                       "A": self.skill_A,
                       "pl": self.skill_pl,
                       "PL_low": self.skill_PL_low,
                       "PL_high": self.skill_PL_high,
                       "e": self.skill_e,
                       "E": self.skill_E,
                       "q": self.skill_q,
                       "Q": self.skill_Q,
                       "p": self.skill_p,
                       "P": self.skill_P}

        self.buff_a = Stats()
        self.buff_A = Stats()
        self.buff_e = Stats()
        self.buff_E = Stats()
        self.buff_q = Stats()
        self.buff_Q = Stats()
        self.buff_p = Stats()
        self.buff_P = Stats()

        self.buffs = {"a": self.buff_a,
                      "A": self.buff_A,
                      "e": self.buff_e,
                      "E": self.buff_E,
                      "q": self.buff_q,
                      "Q": self.buff_Q,
                      "p": self.buff_p,
                      "P": self.buff_P}

    def set_idx(self, idx):
        self.idx = idx
        self.weapon.set_char_idx(idx)
        self.artifact.set_char_idx(idx)

    # def set_team_stats(self, stats):
    #     self.team_stats = stats
    #     self.stats = Stats(self.team_stats[self.idx].reshape(1, Stats.length))

    # def set_on_field(self, on_field):
    #     self.on_field = on_field

    # def attack(self):
    #     return self.stats[0]*(1+self.stats[2]/100)

    # def critical(self):
    #     return 1 + self.stats[10]/100 * self.stats[11]/100

    # def dmg_bonus(self, element):
    #     return 1 + self.stats[element]/100 + self.stats[31]/100

    # def resistance(self, element):
    #     return 1 - self.enemy[element]/100

    # def defence(self, ignorance=0):
    #     d = self.enemy[1] * (1 - self.enemy[11] / 100) * (1 - ignorance / 100)
    #     return 500 * self.level / (d * self.enemy.level + 500 * self.level)

    def constellation_effect(self, *args, **kwargs):
        pass

    # @buff_skill
    # def skill_a(self, counter, buff=()):
    #     scalings = np.array(self.scaling['a'])
    #     a_maximum = scalings.shape[0]
#
    #     scale = ((counter//a_maximum) * np.sum(scalings) + np.sum(scalings[:(counter % a_maximum)]))/100
#
    #     return damage(scale, self.attack(), self.stats[32], self.critical(), self.dmg_bonus('physical'),
    #                   self.resistance('physical'), self.defence())
#
    # @buff_skill
    # def skill_A(self, buff=()):
    #     scale = sum(self.stats['skills']['A'][0])
#
    #     return damage(scale, self.attack(), self.stats[32], self.critical(), self.dmg_bonus('physical'),
    #                   self.resistance('physical'), self.defence())
#
    # @buff_skill
    # def skill_l(self, buff=()):
    #     scale = self.stats['skills']['pl']
#
    #     return damage(scale, self.attack(), self.stats[32], self.critical(), self.dmg_bonus('physical'),
    #                   self.resistance('physical'), self.defence())
#
    # @buff_skill
    # def skill_L(self, buff=()):
    #     scale = self.stats['skills']['PL']
#
    #     return damage(scale, self.attack(), self.stats[32], self.critical(), self.dmg_bonus('physical'),
    #                   self.resistance('physical'), self.defence())
#
    # @buff_skill
    # def skill_e(self, buff=()):
    #     scale = self.stats['skills']['e']
#
    #     return damage(scale, self.attack(), self.stats[32], self.critical(), self.dmg_bonus(self.element),
    #                   self.resistance(self.element), self.defence())
#
    # @buff_skill
    # def skill_E(self, buff=()):
    #     scale = self.stats['skills']['E']
#
    #     return damage(scale, self.attack(), self.stats[32], self.critical(), self.dmg_bonus(self.element),
    #                   self.resistance(self.element), self.defence())
#
    # @buff_skill
    # def skill_q(self, buff=()):
    #     scale = self.stats['skills']['q']
#
    #     return damage(scale, self.attack(), self.stats[32], self.critical(), self.dmg_bonus(self.element),
    #                   self.resistance(self.element), self.defence())
#
    # @buff_skill
    # def skill_Q(self, buff=()):
    #     scale = self.stats['skills']['Q']
#
    #     return damage(scale, self.attack(), self.stats[32], self.critical(), self.dmg_bonus(self.element),
    #                   self.resistance(self.element), self.defence())
#
    # @buff_skill
    # def skill_p(self, buff=()):
    #     scale = self.stats['skills']['p']
#
    #     return damage(scale, self.attack(), self.stats[32], self.critical(), self.dmg_bonus(self.element),
    #                   self.resistance(self.element), self.defence())
#
    # @buff_skill
    # def skill_P(self, buff=()):
    #     scale = self.stats['skills']['P']
#
    #     return damage(scale, self.attack(), self.stats[32], self.critical(), self.dmg_bonus(self.element),
    #                   self.resistance(self.element), self.defence())


if __name__ == "__main__":
    @register_char
    class RaidenShogun(Character):
        def __init__(self, weapon):
            super().__init__(weapon)

    # char = RaidenShogun()
    pass
