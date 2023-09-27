import types

import numpy as np
import torch

from .base_char import register_char, Character
from GTDC.common.stats import Stats, Buff, BasicBuff, ProportionalBuff, Infusion, Skills, PolySkills, ReactionBuff, reaction_buff_check
from GTDC.common.reactions import Bloom, DendroCore, CHAR_LEVEL_COEF


def golden_chalices_react(self, team, skill, stats, enemy, *args, **kwargs):
    # print(args, kwargs)
    core = BountifulCore(kwargs["t"], skill.char, 2, 0.)
    team.dendro_cores.append(core)


class BountifulCore(DendroCore):
    def __init__(self, t, char, coef, increase=0.):
        super(BountifulCore, self).__init__(t, char, 0.5, coef, increase)

    def react(self, team, skill, stats, enemy, *args, **kwargs):
        em = stats[0, 9]
        hp = stats.hp()
        bonus = 16. * em / (em + 2000)

        resistance = enemy["dendro"]

        if resistance < 0:
            resistance = 1 - resistance/200
        elif resistance > 75:
            resistance = 1 / (1 + 4 * resistance/100)
        else:
            resistance = 1 - resistance/100

        self.increase = torch.max(torch.tensor([4., (hp-30000)/1000*0.09]))

        dmg = CHAR_LEVEL_COEF[int(skill.char.level)-1] * self.coef * (1 + bonus + self.increase) * resistance

        return dmg


class GoldenChalicesBounty(ReactionBuff):
    def __init__(self, char):
        super(GoldenChalicesBounty, self).__init__(char, ["Bloom"])

    @reaction_buff_check
    def buff_reaction(self, reaction, team, stats, enemy):
        if isinstance(reaction, Bloom):
            Bloom.react = golden_chalices_react


class SwordDance(Skills):
    def __init__(self, char, scales):
        super(SwordDance, self).__init__(char, scales[0], 'e', 'hydro')
        self.scales = scales
        self.count = 0

        def count_increase(func):
            self.scale = self.scales[self.count]
            def wrapper(obj, *args, **kwargs):
                return func(obj, *args, **kwargs)
            self.count += 1
            if self.count == 3:
                self.count = 0

            return wrapper

        self.calculate = count_increase(calculate)


class WhirlingSteps(Skills):
    def __init__(self, char, scales):
        super(WhirlingSteps, self).__init__(char, scales[0], 'e', 'hydro')
        self.scales = scales
        self.count = 0

        def count_increase(func):
            self.scale = self.scales[self.count]

            def wrapper(obj, *args, **kwargs):
                if self.scale != 0.:
                    return func(obj, *args, **kwargs)
                else:
                    return 0.

            self.count += 1
            if self.count == 3:
                self.count = 0
                self.scales = [0.,0.,0.]

            return wrapper

        self.calculate = count_increase(calculate)


class DanceOfHaftkarsvarInfusion(Infusion):
    def __init__(self, char, scaling):
        # print(bonus)
        a_skill = SwordDance(char, scaling[1:4])
        e_skill = WhirlingSteps(char, scaling[4:7])
        super().__init__(char,
                         {'a': a_skill,
                          'e': e_skill},
                         self_infuse=True)

    def check(self, skill, team=None):
        return (self.char.idx == skill.char.idx) and (skill.skill_type in self.skill_types_from)


def calculate(self, stats, enemy):
    """
    stats:
    """
    scale = self.scale
    maxhp = stats.hp()
    additional = stats.additional()
    critical = stats.critical()
    dmg_bonus = stats.dmg_bonus(self.element_type)
    resistance = enemy[self.element_type]
    if resistance < 0:
        resistance = 1 - resistance / 200
    elif resistance > 75:
        resistance = 1 / (1 + 4 * resistance / 100)
    else:
        resistance = 1 - resistance / 100
    defence = enemy[:, 1] * (1 - enemy[:, 11] / 100)
    def_factor = (1 + self.char.level / 100) * 500 / (
                defence * (1 + enemy.level / 100) + (1 + self.char.level / 100) * 500)
    # print(stats[0,13])
    # print(f"Scale: {scale}\nAttack: {atk.item()}\nAdditional: {additional.item()}\n" +
    #       f"Critical: {critical.item()}\nDamage Bonus: {dmg_bonus.item()}\n" +
    #       f"Resistance: {resistance[0]}\nDefence: {def_factor.item()}\n")
    return (scale / 100 * maxhp + additional) * critical * dmg_bonus * resistance * def_factor


@register_char
class Nilou(Character):
    def __init__(self, weapon, artifact, level=90, constellation=0, name='Nilou',
                 ascension_phase=6, skill_level=(10, 10, 10)):
        super().__init__(weapon, artifact, level, constellation, name, ascension_phase, skill_level)

        self.buff_p = BasicBuff(char=self,
                                 array=torch.tensor([[0., 0., 0.,
                                                      0., 0., 0.,
                                                      0., 0., 0.,
                                                      100., 0., 0., 0., 0., 0.,
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

        self.buff_P = GoldenChalicesBounty(self)

        self.skill_e = Skills(self, self.scaling['e'][self.skill_level[1]-1][0], 'e', self.element)
        self.slill_q.calculate = calculate

        self.infusion = DanceOfHaftkarsvarInfusion(self, self.scaling['e'][self.skill_level[1]-1])

