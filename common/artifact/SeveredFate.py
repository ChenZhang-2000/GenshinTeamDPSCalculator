import numpy as np

from .base_artifact import register_artifact, Artifact
from common.stats import Stats, Buff, BasicBuff, ProportionalBuff


class ECtoDB(ProportionalBuff):
    def __init__(self, char: int, array: np.array = np.zeros((2, Stats.length)),
                 skill_type: str = 'all', field_type: str = 'all', element_type = 'all'):
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
        self.func = lambda x: min(75, x @ array[0]) * array[1]
        super().__init__(char=char, array=np.zeros((2, Stats.length), skill_type=skill_type, field_type=field_type))


@register_artifact
class SeveredFate(Artifact):
    def __init__(self, char_idx):
        super().__init__(char_idx)

        self.two_effect.append([BasicBuff(char_idx,
                                          np.array([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 20, 0.,
                                                     0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]])),
                                'permanent'])

        self.four_effect.append([ECtoDB(char_idx,
                                        np.array([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.25, 0.,
                                                   0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                                  [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                                   1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 0.]]),
                                        skill_type='q'),
                                 'partial'])