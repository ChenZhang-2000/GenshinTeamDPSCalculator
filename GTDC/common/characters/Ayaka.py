import types

import numpy as np
import torch

from .base_char import register_char, Character
from GTDC.common.stats import Stats, Buff, BasicBuff, ProportionalBuff, Infusion, Skills, PolySkills, Debuff


class AyakaInfusion(Infusion):
    def __init__(self, char):
        super().__init__(char=char, skill_infused={}, self_infuse=False, infuse_element="cryo")
        self.skill_types_from = ["a", "A", "pl", "PL"]

    def check(self, skill, team=None):
        return skill.skill_type in self.skill_types_from


@register_char
class Ayaka(Character):
    def __init__(self, weapon, artifact, level=90, constellation=0, name='Ayaka',
                 ascension_phase=6, skill_level=(10, 10, 10)):
        super().__init__(weapon, artifact, level, constellation, name, ascension_phase, skill_level)

        self.infusion = AyakaInfusion(self)

        q_scale = self.scaling['q'][self.skill_level[2]-1]
        # print(q_scale)
        self.skill_q = Skills(self, q_scale[0]*19 + q_scale[1], 'q', self.element)

        self.buff_p = BasicBuff(char=self,
                                skill_type=['a', 'A'],
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
                                                     30.,
                                                     0.]]))
        self.buff_P = BasicBuff(char=self,
                                array=torch.tensor([[0., 0., 0.,
                                                     0., 0., 0.,
                                                     0., 0., 0.,
                                                     0., 0., 0., 0., 0., 0.,
                                                     0., 0.,
                                                     0., 0.,
                                                     0., 0.,
                                                     18., 0.,
                                                     0., 0.,
                                                     0., 0.,
                                                     0., 0.,
                                                     0., 0.,
                                                     0.,
                                                     0.]]))
        self.buff_c4 = Debuff(torch.tensor([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 30.]]))
        self.buff_c6 = BasicBuff(char=self,
                                 skill_type='A',
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
                                                      298.,
                                                      0.]]))

        self.buff_p.valid = lambda self, skill, team, on_field: self.char.idx == skill.char.idx
        self.buff_P.valid = lambda self, skill, team, on_field: self.char.idx == skill.char.idx
        self.buff_c6.valid = lambda self, skill, team, on_field: self.char.idx == skill.char.idx

        self.skills = {"a": self.skill_a,
                       "A": self.skill_A,
                       "pl": self.skill_pl,
                       "PL_low": self.skill_PL_low,
                       "PL_high": self.skill_PL_high,
                       "e": self.skill_e,
                       "q": self.skill_q}

        self.buffs = {"p": self.buff_p,
                      "P": self.buff_P}

        self.constellation_effect()

    def constellation_effect(self, *args, **kwargs):
        if self.constellation >= 2:
            self.skill_q.scale *= 1.4

        if self.constellation >= 4:
            self.buffs['c4'] = self.buff_c4

        if self.constellation >= 6:
            self.buffs['c6'] = self.buff_c6


