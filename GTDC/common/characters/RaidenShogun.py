import types

import numpy as np
import torch

from .base_char import register_char, Character
from GTDC.common.stats import Stats, Buff, BasicBuff, ProportionalBuff, Infusion, Skills, PolySkills


def calculate(self, stats, enemy):
    """
    stats:
    """
    scale = self.scale
    atk = stats.atk()
    additional = stats.additional()
    critical = stats.critical()
    dmg_bonus = stats.dmg_bonus(self.element_type)
    resistance = enemy[self.element_type]
    if resistance < 0:
        resistance = 1 - resistance / 200
    elif resistance > 75:
        resistance = 1 / (1 + 4 * resistance / 100)
    else:
        resistance = 1 - resistance / 100
    defence = enemy[:, 1] * (1 - enemy[:, 11] / 100) * 0.4
    def_factor = (1 + self.char.level/100) * 500 / (defence * (1 + enemy.level/100) + (1 + self.char.level/100) * 500)
    # print(stats[0,13])
    # print(f"Scale: {scale}\nAttack: {atk.item()}\nAdditional: {additional.item()}\n" +
    #       f"Critical: {critical.item()}\nDamage Bonus: {dmg_bonus.item()}\n" +
    #       f"Resistance: {resistance[0]}\nDefence: {def_factor.item()}\n")
    return (scale/100 * atk + additional) * critical * dmg_bonus * resistance * def_factor


class RaidenInfusion(Infusion):
    def __init__(self, char, scaling, stacks):
        bonus = scaling[-1][0] * stacks
        # print(bonus)
        super().__init__(char, {'a': PolySkills(char, [sum(i)+bonus*len(i) for i in scaling[:5]], 'q', 'electro'),
                                'A': Skills(char, sum(scaling[5])+bonus*2, 'q', 'electro'),
                                'pl': Skills(char, sum(scaling[6])+bonus, 'q', 'electro'),
                                'PL_low': Skills(char, scaling[7][0]+bonus, 'q', 'electro'),
                                'PL_high': Skills(char, scaling[7][1]+bonus, 'q', 'electro')}, self_infuse=True)
        self.char.skill_q.scale += scaling[-2][0] * stacks

    def check(self, skill, team=None):
        return (self.char.idx == skill.char.idx) and (skill.skill_type in self.skill_types_from)


class Buff_e(BasicBuff):
    def __init__(self, char):
        super().__init__(char=char,
                         skill_type={'q', 'Q'},
                         array=torch.tensor([[0., 0., 0.,
                                              0., 0., 0.,
                                              0., 0., 0.,
                                              0., 0., 0., 0., 0., 0.,
                                              0., 0.,
                                              0., 0.,
                                              0., 0.,
                                              0., 0.,
                                              0., 0.,
                                              0., 0.,
                                              0., 0.,
                                              0., 0.,
                                              0.,
                                              0.]]))

    def valid(self, skill, team, on_field):
        # print(self.char.idx == team.on_field)
        return on_field

    def update(self, energy=90):
        # print(type(energy))
        if energy != '':
            self.data[0, 31] = int(energy) * 0.3


class BuffConstellation4(BasicBuff):
    def __init__(self, char):
        super().__init__(char=char,
                         skill_type={'q', 'Q'},
                         array=torch.tensor([[0., 0., 30.,
                                              0., 0., 0.,
                                              0., 0., 0.,
                                              0., 0., 0., 0., 0., 0.,
                                              0., 0.,
                                              0., 0.,
                                              0., 0.,
                                              0., 0.,
                                              0., 0.,
                                              0., 0.,
                                              0., 0.,
                                              0., 0.,
                                              0.,
                                              0.]]))

    def valid(self, skill, team, on_field):
        return self.char.idx != skill.char.idx


class BuffP(ProportionalBuff):
    def __init__(self, char):
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
        # assert array.shape == (2, Stats.length)
        mask = torch.tensor([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., -100., 0., 0.,
                              0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]])
        array = torch.sparse_coo_tensor([[19], [13]], [0.4], (Stats.length, Stats.length))
        super().__init__(char=char)
        self.func = lambda x:  (array @ (x+mask).T).T


@register_char
class RaidenShogun(Character):
    def __init__(self, weapon, artifact, level=90, constellation=0, name='Raiden Shogun',
                 ascension_phase=6, skill_level=(10, 10, 10)):
        super().__init__(weapon, artifact, level, constellation, name, ascension_phase, skill_level)
        self.buff_P = BuffP(self)

        self.buff_e = Buff_e(self)
        self.buff_c4 = BasicBuff(char=self,
                                 array=torch.tensor([[0., 0., 10.,
                                                      0., 0., 0.,
                                                      0., 0., 0.,
                                                      0., 0., 0., 0., 0., 0.,
                                                      0., 0.,
                                                      0., 0.,
                                                      0., 0.,
                                                      0., 0.,
                                                      0., 0.,
                                                      0., 0.,
                                                      0., 0.,
                                                      0., 0.,
                                                      0.,
                                                      0.]]))

        self.skill_e = Skills(self, self.scaling['e'][self.skill_level[1]-1][1], 'e', 'electro')
        self.skill_e.first_skill = Skills(self, self.scaling['e'][self.skill_level[1]-1][0], 'e', 'electro')
        self.skill_e.first_particular = True

        self.infusion = RaidenInfusion(self, self.scaling['other'][self.skill_level[2]-1], 60)

        #     Infusion(self, {'a': PolySkills(self, [sum(i) for i in self.scaling['other'][:5]], 'a', 'electro'),
        #                                 'A': Skills(self, sum(self.scaling['other'][5]), 'A', 'electro'),
        #                                 'pl': Skills(self, sum(self.scaling['other'][6]), 'pl', 'electro'),
        #                                 'PL_low': Skills(self, sum(self.scaling['other'][7][0]), 'PL_low', 'electro'),
        #                                 'PL_high': Skills(self, sum(self.scaling['other'][7][1]), 'PL_high', 'electro')})

        self.skills = {"a": self.skill_a,
                       "A": self.skill_A,
                       "pl": self.skill_pl,
                       "PL_low": self.skill_PL_low,
                       "PL_high": self.skill_PL_high,
                       "e": self.skill_e,
                       "E": self.skill_E,
                       "q": self.skill_q}

        self.buffs = {"e": self.buff_e,
                      "P": self.buff_P,
                      # "w": self.weapon.buffs,
                      "infusion": self.infusion,
                      "附魔": self.infusion}

        self.constellation_effect()

    def constellation_effect(self, *args, **kwargs):
        if self.constellation >= 2:
            for skill in [self.skill_q, * self.infusion.skills_infused.values()]:
                if isinstance(skill, PolySkills):
                    for s in skill.skills:
                        s.calculate = types.MethodType(calculate, s)
                    continue
                skill.calculate = types.MethodType(calculate, skill)
        if self.constellation >= 4:
            self.buffs['c4'] = self.buff_c4

