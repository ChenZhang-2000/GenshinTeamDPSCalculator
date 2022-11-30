from .reaction import Amplifying, register_reaction


@register_reaction
class Vaporize(Amplifying):
    def __init__(self):
        super().__init__()


@register_reaction
class Melt(Amplifying):
    def __init__(self):
        super().__init__()
