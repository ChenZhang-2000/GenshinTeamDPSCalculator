import numpy as np
import torch

from .base_char import register_char, Character
from common.stats import Stats, Buff, BasicBuff, ProportionalBuff, Infusion, Skills, PolySkills, damage


def calculate(self, stats, enemy):
    """
    stats:
    """
    scale = self.scale
    atk = stats[0] * (1 + stats[2] / 100) + stats[1]
    additional = stats[32]
    critical = 1 + (stats[9] * stats[10] / 10000)
    dmg_bonus = 1 + (stats[self.element_type] / 100) + (stats[31] / 100)
    resistance = enemy[self.element_type]
    if resistance < 0:
        resistance = 1 - resistance / 200
    elif resistance > 75:
        resistance = 1 / (1 + 4 * resistance / 100)
    else:
        resistance = 1 - resistance / 100
    defence = enemy[1] * (1 - enemy[11] / 100) * 0.4

    return damage(scale, atk, additional, critical, dmg_bonus, resistance, defence)


class RaidenInfusion(Infusion):
    def __init__(self, char, scaling, stacks):
        bonus = 1.31 * stacks
        super().__init__(char, {'a': PolySkills(self, [sum(i)+bonus*len(i) for i in scaling[:5]], 'a', 'electro'),
                                'A': Skills(self, sum(scaling[5])+bonus*2, 'A', 'electro'),
                                'pl': Skills(self, sum(scaling[6])+bonus, 'pl', 'electro'),
                                'PL_low': Skills(self, scaling[7][0]+bonus, 'PL_low', 'electro'),
                                'PL_high': Skills(self, scaling[7][1]+bonus, 'PL_high', 'electro')})
        self.char.skill_q.scale += 7 * stacks


class Buff_e(BasicBuff):
    def __init__(self):
        super().__init__(char=self,
                         skill_type={'q', 'Q'},
                         array=torch.tensor([0., 0., 0.,
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
                                             0.]))

    def valid(self, skill, team):
        return self.char.idx == team.on_field

    def update(self, energy=80):
        self.data[31] = energy * 0.3


class BuffConstellation4(BasicBuff):
    def __init__(self):
        super().__init__(char=self,
                         skill_type={'q', 'Q'},
                         array=torch.tensor([0., 0., 30.,
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
                                             0.]))

    def valid(self, skill, team):
        return self.char.idx != skill.char.idx


class BuffP(ProportionalBuff):
    def __init__(self, char: int, array: torch.tensor = torch.zeros(2, Stats.length),
                 skill_type: str = 'all'):
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
        self.func = lambda x: (x+mask) @ array[0] * array[1]
        super().__init__(char=char, array=torch.zeros(2, Stats.length), skill_type=skill_type)


@register_char
class RaidenShogun(Character):
    def __init__(self, weapon, enemy, artifact, level=90, constellation=0):
        super().__init__(weapon, enemy, artifact, level, constellation)
        self.buff_P = BuffP(self.idx, torch.tensor([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.4, 0., 0., 0.,
                                                     0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                                    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                                     0., 0., 0., 0., -1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]]))

        self.buff_e = Buff_e()
        self.buff_cons_4 = BasicBuff(char=self,
                                     element_type='q',
                                     array=torch.tensor([0., 0., 0.,
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
                                                         0.]))

        self.skill_e_init = self.skill_e = Skills(self, 210.96, 'e', 'electro')
        self.skill_e.scale = 75.6

        self.infusion = RaidenInfusion(self, self.scaling['other'], 60)

        #     Infusion(self, {'a': PolySkills(self, [sum(i) for i in self.scaling['other'][:5]], 'a', 'electro'),
        #                                 'A': Skills(self, sum(self.scaling['other'][5]), 'A', 'electro'),
        #                                 'pl': Skills(self, sum(self.scaling['other'][6]), 'pl', 'electro'),
        #                                 'PL_low': Skills(self, sum(self.scaling['other'][7][0]), 'PL_low', 'electro'),
        #                                 'PL_high': Skills(self, sum(self.scaling['other'][7][1]), 'PL_high', 'electro')})

        self.skills = [self.skill_a, self.skill_A,
                       self.skill_pl, self.skill_PL_low, self.skill_PL_high,
                       self.skill_e_init, self.skill_e,
                       self.skill_q]

    def constellation_effect(self, *args, **kwargs):
        if self.constellation >= 2:
            for skill in [self.skill_q, *self.infusion.skill_infused.keys()]:
                skill.calculate = calculate
        if self.constellation >= 3:
            self.skill_q.scale += 130.26
            a_bonus = [13.72, 13.49, 16.52, 18.89, 22.69]
            for i in range(5):
                self.infusion.skill_infused['a'].skills[i].scale += a_bonus[i]
            self.infusion.skill_infused['A'].scale += 41.71
            self.infusion.skill_infused['pl'].scale += 26.76
            self.infusion.skill_infused['PL_low'].scale += 53.52
            self.infusion.skill_infused['PL_high'].scale += 66.84
        if self.constellation >= 4:
            pass
        if self.constellation >= 5:
            self.skill_e_init.scale += 38.09
            self.skill_e.scale += 13.65

