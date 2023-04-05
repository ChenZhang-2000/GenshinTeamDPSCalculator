import numpy as np
import torch

from .base_weapon import register_weapon, Weapon
from GTDC.common.stats import Stats, Buff, BasicBuff, ProportionalBuff, Skills


@register_weapon
class SkywardBlade(Weapon):
    def __init__(self, affix=1):
        super().__init__(affix)

    def init_char(self, char):
        self.char = char
        self.permanent_buffs.append(BasicBuff(self.char,
                                    torch.tensor([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 3. + self.affix, 0., 0., 0., 0., 0., 0.,
                                                   0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]])))

        self.skills.append(Skills(self.char, 15 + self.affix * 5, "other", "physical"))
