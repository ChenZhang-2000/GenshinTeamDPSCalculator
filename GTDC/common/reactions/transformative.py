import torch

from .reaction import Transformative, Catalyze, Blooming, DendroCore, register_reaction, CHAR_LEVEL_COEF, ReactionError


@register_reaction
class Frozen(Transformative):
    def __init__(self, increase=0.):
        super().__init__("cryo", 0., increase)


@register_reaction
class Overloaded(Transformative):
    def __init__(self, increase=0.):
        super().__init__("pyro", 2., increase)


@register_reaction
class ElectroCharged(Transformative):
    def __init__(self, increase=0.):
        super().__init__("electro", 1.2, increase)


@register_reaction
class Superconduct(Transformative):
    def __init__(self, increase=0.):
        super().__init__("cryo", 0.5, increase)


@register_reaction
class Shattered(Transformative):
    def __init__(self, increase=0.):
        super().__init__("physical", 1.5, increase)


@register_reaction
class Quicken(Catalyze):
    def __init__(self, increase=0.):
        super().__init__(0, increase)


@register_reaction
class Aggravate(Catalyze):
    def __init__(self, increase=0.):
        super().__init__(1.15, increase)


@register_reaction
class Spread(Catalyze):
    def __init__(self, increase=0.):
        super().__init__(1.25, increase)


@register_reaction
class Burning(Transformative):
    def __init__(self, increase=0.):
        super().__init__("pyro", 0.25, increase)


@register_reaction
class Bloom(Blooming):
    def __init__(self, increase=0.):
        super().__init__(2, increase)

    def react(self, team, skill, stats, enemy, *args, **kwargs):
        # print(args, kwargs)
        core = DendroCore(kwargs["t"], skill.char, 6, 2, 0.)
        team.dendro_cores.append(core)


@register_reaction
class Hyperbloom(Blooming):
    def __init__(self, increase=0.):
        super().__init__(3., increase)


@register_reaction
class Burgeon(Blooming):
    def __init__(self, increase=0.):
        super().__init__(3., increase)


@register_reaction
class Swirl(Transformative):
    def __init__(self, increase=0.):
        super().__init__("anemo", 0.6, increase)


@register_reaction
class Crystallize(Transformative):
    def __init__(self, increase=0.):
        super().__init__("geo", 0., increase)
