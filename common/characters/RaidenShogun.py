import numpy as np
import torch

from .base_char import register_char, Character, buff_skill
from common.stats import Stats, Buff, BasicBuff, ProportionalBuff


class BuffP(ProportionalBuff):
    def __init__(self, char: int, array: torch.tensor = torch.zeros(2, Stats.length),
                 skill_type: str = 'all', field_type: str = 'all', element_type='all'):
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
        super().__init__(char=char, array=torch.zeros(2, Stats.length), skill_type=skill_type, field_type=field_type)


@register_char
class RaidenShogun(Character):
    def __init__(self, weapon, enemy, artifact, level=90):
        super().__init__(weapon, enemy, artifact, level)
        self.buff_P = BuffP(self.idx, torch.tensor([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.4, 0., 0., 0.,
                                                     0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                                    [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                                     0., 0., 0., 0., -1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]]))

    @buff_skill
    def skill_e(self, buff=()):
        pass