import torch

from .base_artifact import register_artifact, Artifact
from GTDC.common.stats import Stats, Buff, BasicBuff, ProportionalBuff


class ECtoDB(ProportionalBuff):
    def __init__(self, char: int, ):
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
        array = torch.sparse_coo_tensor([[31], [13]], [0.25], (Stats.length, Stats.length))
        super().__init__(char=char, array=array, skill_type='q')
        # self.func = lambda x: (array @ x.T).T

        max_mask = torch.tensor([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0, 0, 0,
                                  0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 75., 0.]])

        def func(x):
            y = (array @ (x).T).T
            # print(y.shape)
            y = y * (y <= max_mask) + max_mask * (y > max_mask)
            return y

        self.func = func


@register_artifact
class SeveredFate(Artifact):
    def __init__(self, char):
        super().__init__(char)

        self.two_effect.append((BasicBuff(char,
                                          torch.tensor([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 20, 0.,
                                                     0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]])),
                                'permanent'))

        self.four_effect.append((ECtoDB(char),
                                 'permanent'))
