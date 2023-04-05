import numpy as np
import torch

from .base_weapon import register_weapon, Weapon
from GTDC.common.stats import Stats, Buff, BasicBuff, ProportionalBuff


class ECtoATK(ProportionalBuff):
    def __init__(self, char, affix):
        """
        char: index of the characters in the team
        """
        # print(array)
        # assert array.shape == (2, Stats.length)
        mask = torch.tensor([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., -100., 0, 0, 0,
                              0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]]).double()
        array = torch.sparse_coo_tensor([[2], [13]], [0.07 * (3+affix)], (Stats.length, Stats.length)).double()
        super().__init__(char=char)

        def func(x):
            y = (array @ (x + mask).T).T
            excess = (y > 70 + 10 * affix)
            y[excess] = 70 + 10 * affix
            return y

        self.func = func


@register_weapon
class EngulfingLightning(Weapon):
    def __init__(self, affix=1):
        super().__init__(affix)

    def init_char(self, char):
        self.char = char
        self.permanent_buffs.append(ECtoATK(self.char, self.affix))

        self.buffs.append(BasicBuff(self.char,
                                    torch.tensor([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 30, 0., 0., 0.,
                                                   0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]])))
