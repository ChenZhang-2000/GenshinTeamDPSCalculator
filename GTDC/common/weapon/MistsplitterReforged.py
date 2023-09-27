import numpy as np
import torch

from .base_weapon import register_weapon, Weapon
from GTDC.common.exception import InvalidValue
from GTDC.common.stats import Stats, Buff, BasicBuff, ProportionalBuff, Skills, ELEMENT_IDX_MAP


class MistsplitterReforgedElementalDB(BasicBuff):
    def __init__(self, char):
        element = char.element
        self.element_idx = ELEMENT_IDX_MAP[element] * 2 + 15
        super().__init__(char=char,
                         array=torch.tensor([[0., 0., 0.,
                                              0., 0., 0.,
                                              0., 0., 0.,
                                              0., 0., 0., 0., 0., 0.,
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

    def update(self, stack=3):
        if stack == 0:
            pass
        elif stack == 1:
            self.data[0, self.element_idx] = 6 + self.char.weapon.affix * 2
        elif stack == 2:
            self.data[0, self.element_idx] = 12 + self.char.weapon.affix * 4
        elif stack == 3:
            self.data[0, self.element_idx] = 21 + self.char.weapon.affix * 7
        else:
            raise InvalidValue(f"Invalid Stacks {stack}")


@register_weapon
class MistsplitterReforged(Weapon):
    def __init__(self, affix=1):
        super().__init__(affix)

    def init_char(self, char):
        self.char = char
        self.permanent_buffs.append(BasicBuff(self.char,
                                    torch.tensor([[0., 0., 0., 0., 0., 0., 0., 0., 0.,
                                                   0., 0., 0., 0., 0., 0.,
                                                   9. + 3 * self.affix, 0.,
                                                   9. + 3 * self.affix, 0.,
                                                   9. + 3 * self.affix, 0.,
                                                   9. + 3 * self.affix, 0.,
                                                   9. + 3 * self.affix, 0.,
                                                   9. + 3 * self.affix, 0.,
                                                   9. + 3 * self.affix, 0.,
                                                   0., 0.,
                                                   0., 0.]])))

        self.buffs.append(MistsplitterReforgedElementalDB(self.char))
