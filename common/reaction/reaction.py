REACTION_FACTORY = {}


def register_reaction(cls):
    cls_name = cls.__class__.__name__

    def register(cls):
        REACTION_FACTORY[cls_name] = cls

    return register(cls)


class Reaction:
    pass


class Amplifying(Reaction):
    def __init__(self):
        pass


class Transformative(Reaction):
    def __init__(self):
        pass
