import numpy as np
import torch

from .base_weapon import register_weapon, Weapon
from GTDC.common.stats import Stats, Buff, BasicBuff, ProportionalBuff


class ECtoATK(ProportionalBuff):
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
        mask = torch.tensor([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., -100., 0, 0, 0,
                              0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]]).double()
        array = torch.sparse_coo_tensor([[2], [13]], [0.28], (Stats.length, Stats.length)).double()
        super().__init__(char=char)
        self.func = lambda x: (array @ (x+mask).T).T


@register_weapon
class EngulfingLightning(Weapon):
    def __init__(self, affix=1):
        super().__init__(affix)

    def init_char(self, char):
        self.char = char
        self.permanent_buffs.append(ECtoATK(self.char))

        self.buffs.append(BasicBuff(self.char,
                                    torch.tensor([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 30, 0., 0., 0.,
                                                   0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]])))
