import json
import numpy as np

from common.stats import Stats, Buff, BasicBuff, ProportionalBuff


ARTIFACT_FACTORY = {}


def register_artifact(cls):
    cls_name = cls.__name__

    def register(cls):
        ARTIFACT_FACTORY[cls_name] = cls

    return register(cls)


class Artifact(object):
    def __init__(self, char_idx):
        self.char_idx = char_idx
        self.two_effect = [[BasicBuff, 'permanent']]
        self.four_effect = [[BasicBuff, 'permanent']]


class ArtifactSet(object):
    def __init__(self, stats: np.array = np.zeros((1,30)), two_set: type = Artifact, four_set: type = Artifact):

        self.two_set = two_set
        self.four_set = four_set

        self.char_idx = 0
        self.stats = stats
        self.permanent_buffs = []
        self.partial_buffs = []

    def set_char_idx(self, idx):
        self.char_idx = idx

        t = self.two_set(idx)
        f = self.four_set(idx)

        if self.two_set == self.four_set:
            buffs = t.two_effect + t.four_effect
        else:
            buffs = t.two_effect + f.two_effect

        for buff, buff_type in buffs:
            if buff_type == 'permanent':
                self.permanent_buffs.append(buff)
            elif buff_type == 'partial':
                self.partial_buffs.append(buff)
