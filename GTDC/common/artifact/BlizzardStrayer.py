import torch

from .base_artifact import register_artifact, Artifact
from GTDC.common.stats import Stats, Buff, BasicBuff, ProportionalBuff


class BlizzardStrayerFour(BasicBuff):
    def __init__(self, char):
        super().__init__(char=char,
                         array=torch.tensor([[0., 0., 0.,
                                              0., 0., 0.,
                                              0., 0., 0.,
                                              0., 40., 0., 0., 0., 0.,
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

    def update(self, stack=2):
        if stack == 1:
            self.data[0, 10] = 20


@register_artifact
class BlizzardStrayer(Artifact):
    def __init__(self, char):
        super().__init__(char)

        self.two_effect.append((BasicBuff(char,
                                          torch.tensor([[0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                                         0., 0., 0., 0., 0., 0.,
                                                         0., 0., 0., 0.,
                                                         0., 0., 0., 0.,
                                                         15., 0., 0., 0.,
                                                         0., 0., 0., 0.,
                                                         20., 0.]])),
                                'permanent'))

        self.four_effect.append((BlizzardStrayerFour(char), 'partial'))

