import os
import json

import torch

REACTION_FACTORY = {}

LEVEL_COEF = json.load(open(os.path.join(os.path.dirname(__file__), f'coefficient.json')))
CHAR_LEVEL_COEF = LEVEL_COEF["character"]


class ReactionError(Exception):
    def __init__(self, element_type, reaction):
        self.element_type = element_type
        self.reaction = reaction


def register_reaction(cls):
    cls_name = cls.__name__

    def register(cls):
        REACTION_FACTORY[cls_name] = cls
        return cls

    return register(cls)


class Reaction:
    def __init__(self, increase=0.):
        self.increase = increase

    def react(self, team, skill, stats, enemy, *args, **kwargs):
        pass


class Amplifying(Reaction):
    def __init__(self, increase=0.):
        super().__init__(increase)

    def react(self, team, skill, stats, enemy, *args, **kwargs):
        return 1.


class Transformative(Reaction):
    def __init__(self, element_type, coef, increase=0.):
        super().__init__(increase)
        self.element_type = element_type
        self.coef = coef

    def react(self, team, skill, stats, enemy, *args, **kwargs):
        em = stats[0, 9]
        # print(em)
        bonus = 16. * em / (em + 2000)

        resistance = enemy[self.element_type]
        if resistance < 0:
            resistance = 1 - resistance/200
        elif resistance > 75:
            resistance = 1 / (1 + 4 * resistance/100)
        else:
            resistance = 1 - resistance/100

        # print(resistance)
        # print(CHAR_LEVEL_COEF[int(skill.char.level)-1])
        dmg = CHAR_LEVEL_COEF[int(skill.char.level)-1] * self.coef * (1 + bonus + self.increase) * resistance

        return dmg


class Catalyze(Reaction):
    def __init__(self, coef, increase=0.):
        super().__init__(increase)
        self.coef = coef

    def react(self, team, skill, stats, enemy, *args, **kwargs):
        em = stats[0, 9]
        bonus = 5. * em / (em + 1200)

        dmg_bonus = CHAR_LEVEL_COEF[int(skill.char.level)-1] * self.coef * (1 + bonus + self.increase)

        return dmg_bonus


class Blooming(Reaction):
    def __init__(self, coef, increase=0.):
        super().__init__(increase)
        self.coef = coef

    def react(self, team, skill, stats, enemy, *args, **kwargs):
        dmg = torch.Tensor([0.])

        other_cores = []

        for dendro_core in team.dendro_cores:
            if type(dendro_core) == DendroCore:
                dmg += dendro_core.react(team, skill, stats, enemy)
            else:
                other_cores.append(dendro_core)

        team.dendro_cores = other_cores

        return dmg


class DendroCore(Blooming):
    def __init__(self, t, char, duration, coef, increase=0.):
        self.start_time = t
        self.char = char
        self.duration = duration
        super(DendroCore, self).__init__(coef, increase)

    def react(self, team, skill, stats, enemy, *args, **kwargs):
        em = stats[0, 9]
        bonus = 16. * em / (em + 2000)

        resistance = enemy["dendro"]

        if resistance < 0:
            resistance = 1 - resistance/200
        elif resistance > 75:
            resistance = 1 / (1 + 4 * resistance/100)
        else:
            resistance = 1 - resistance/100

        dmg = CHAR_LEVEL_COEF[int(skill.char.level)-1] * self.coef * (1 + bonus + self.increase) * resistance

        return dmg

