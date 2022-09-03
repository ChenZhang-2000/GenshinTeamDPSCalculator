

from .stats import Skills


REACTION_FACTORY = {}


def register_reaction(cls):
    cls_name = cls.__name__

    def register(cls):
        REACTION_FACTORY[cls_name] = cls

    return register(cls)


class Reaction: ...


@register_reaction
class Amplifying(Reaction): ...


@register_reaction
class Transformative(Reaction): ...


@register_reaction
class Vaporize(Amplifying): ...


@register_reaction
class Melt(Amplifying): ...


@register_reaction
class Frozen(): ...


@register_reaction
class Overloaded(Transformative): ...


@register_reaction
class ElectroCharged(Transformative): ...


@register_reaction
class Superconduct(Transformative): ...


@register_reaction
class Quicken(Transformative): ...


@register_reaction
class Aggravate(Transformative): ...


@register_reaction
class Spread(Transformative): ...


@register_reaction
class Burning(Transformative): ...


@register_reaction
class Bloom(Transformative): ...


@register_reaction
class Burgeon(Transformative): ...


@register_reaction
class Hyperbloom(Transformative): ...


@register_reaction
class Swirl(Transformative): ...


@register_reaction
class Crystallize(Transformative): ...
