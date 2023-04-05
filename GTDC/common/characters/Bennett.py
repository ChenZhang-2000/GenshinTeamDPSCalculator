import types

import numpy as np
import torch

from .base_char import register_char, Character
from GTDC.common.stats import Stats, Buff, BasicBuff, ProportionalBuff, Infusion, Skills, PolySkills


class Buffq(ProportionalBuff):
    def __init__(self, char):
        scale = char.scaling['other'][char.skill_level[2]-1][0]
        if char.constellation >= 1:
            scale += 20
        array = torch.sparse_coo_tensor([[1], [0]],
                                        [scale],
                                        (Stats.length, Stats.length)).double()
        super().__init__(char=char, array=array)

    def valid(self, skill, team, on_field):
        return on_field


class BennettInfusion(Infusion):
    def __init__(self, char):
        super().__init__(char=char, skill_infused={}, self_infuse=False, infuse_element="pyro")
        self.skill_types_from = ["a", "A", "pl", "PL"]

    def check(self, skill, team=None):
        return skill.skill_type in self.skill_types_from


@register_char
class Bennett(Character):
    def __init__(self, weapon, artifact, level=90, constellation=0, name='Bennett',
                 ascension_phase=6, skill_level=(10, 10, 10)):
        super().__init__(weapon, artifact, level, constellation, name, ascension_phase, skill_level)

        self.buff_q = Buffq(self)

        self.infusion = BennettInfusion(self)

        self.skills = {"a": self.skill_a,
                       "A": self.skill_A,
                       "pl": self.skill_pl,
                       "PL_low": self.skill_PL_low,
                       "PL_high": self.skill_PL_high,
                       "e": self.skill_e,
                       "E": self.skill_E,
                       "q": self.skill_q}

        self.buffs = {"q": self.buff_q,
                      }

        self.constellation_effect()

    def constellation_effect(self, *args, **kwargs):
        if self.constellation >= 4:
            pass
        if self.constellation >= 6:
            self.buffs["infusion"] = self.infusion
            self.buffs["附魔"] = self.infusion
