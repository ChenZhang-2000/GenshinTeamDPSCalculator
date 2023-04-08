import torch

from .base_artifact import register_artifact, Artifact
from GTDC.common.stats import Stats, Buff, BasicBuff, ProportionalBuff


@register_artifact
class NoblesseOblige(Artifact):
    def __init__(self, char):
        super().__init__(char)

        self.two_effect.append((BasicBuff(char,
                                          torch.tensor([[0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                                         0., 0., 0., 0., 0., 0.,
                                                         0., 0., 0., 0.,
                                                         0., 0., 0., 0.,
                                                         0., 0., 0., 0.,
                                                         0., 0., 0., 0.,
                                                         20., 0.]]),
                                          "q"),
                                'permanent'))

        self.four_effect.append((BasicBuff(char,
                                           torch.tensor([[0., 0., 20., 0., 0., 0., 0., 0., 0.,
                                                          0., 0., 0., 0., 0., 0.,
                                                          0., 0., 0., 0.,
                                                          0., 0., 0., 0.,
                                                          0., 0., 0., 0.,
                                                          0., 0., 0., 0.,
                                                          0., 0.]])),
                                'partial'))
