from .reaction import Amplifying, register_reaction, ReactionError


@register_reaction
class Vaporize(Amplifying):
    def __init__(self, increase=0.):
        super().__init__(increase)

    def react(self, team, skill, stats, enemy, *args, **kwargs):
        em = stats[0, 9]
        bonus = 2.78 * em / (em + 1400)

        if skill.element_type == "hydro":
            reaction_factor = 2.
        elif skill.element_type == "pyro":
            reaction_factor = 1.5
        else:
            raise ReactionError(skill.element_type, "Vaporize")

        return reaction_factor * (1 + bonus + self.increase)


@register_reaction
class Melt(Amplifying):
    def __init__(self, increase=0.):
        super().__init__()
        self.increase = increase

    def react(self, team, skill, stats, enemy, *args, **kwargs):
        em = stats[0, 9]
        bonus = 2.78 * em / (em + 1400)

        if skill.element_type == "pyro":
            reaction_factor = 2.
        elif skill.element_type == "cryo":
            reaction_factor = 1.5
        else:
            raise ReactionError(skill.element_type, "Melt")

        return reaction_factor * (1 + bonus + self.increase)
