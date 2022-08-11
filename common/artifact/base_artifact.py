import json
import torch

from common.stats import Stats, Buff, BasicBuff, ProportionalBuff, STATS_LENGTH


ARTIFACT_FACTORY = {}


def register_artifact(cls):
    cls_name = cls.__name__

    def register(cls):
        ARTIFACT_FACTORY[cls_name] = cls

    return register(cls)


class Artifact(object):
    def __init__(self, char_idx):
        self.char_idx = char_idx
        self.two_effect = []
        self.four_effect = []


class ArtifactSet(object):
    def __init__(self, stats: torch.tensor = torch.zeros(1, STATS_LENGTH),
                 two_set: type = Artifact, four_set: type = Artifact):

        self.two_set = two_set
        self.four_set = four_set

        self.stats = Stats(stats)
        # print(type(self.stats))
        self.permanent_buffs = []
        self.buffs = []

    def set_stats(self, stats: Stats):
        self.stats = stats

    def init_char(self, char):
        self.char = char
        t = self.two_set(char)
        f = self.four_set(char)

        if self.two_set == self.four_set:
            # print(1)
            buffs = t.two_effect + t.four_effect
        else:
            # print(1)
            buffs = t.two_effect + f.two_effect
        # print(buffs)
        for buff, buff_type in buffs:
            # print(buff)
            if buff_type == 'permanent':
                # print(buff)
                self.permanent_buffs.append(buff)
            elif buff_type == 'partial':
                self.buffs.append(buff)
