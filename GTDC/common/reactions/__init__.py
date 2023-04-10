from .reaction import Reaction, Amplifying, Transformative, Catalyze, Blooming, REACTION_FACTORY
from .amplifying import Vaporize, Melt
from .transformative import Frozen, Overloaded, ElectroCharged, Superconduct, Swirl, Crystallize, Shattered, Burning
from .transformative import Quicken, Aggravate, Spread
from .transformative import Bloom, DendroCore, Burgeon, Hyperbloom


Vaporize        = REACTION_FACTORY["Vaporize"]
Melt            = REACTION_FACTORY["Melt"]
Frozen          = REACTION_FACTORY["Frozen"]
Overloaded      = REACTION_FACTORY["Overloaded"]
ElectroCharged  = REACTION_FACTORY["ElectroCharged"]
Superconduct    = REACTION_FACTORY["Superconduct"]
Swirl           = REACTION_FACTORY["Swirl"]
Crystallize     = REACTION_FACTORY["Crystallize"]
Shattered       = REACTION_FACTORY["Shattered"]
Burning         = REACTION_FACTORY["Burning"]
Quicken         = REACTION_FACTORY["Quicken"]
Aggravate       = REACTION_FACTORY["Aggravate"]
Spread          = REACTION_FACTORY["Spread"]
Bloom           = REACTION_FACTORY["Bloom"]
Burgeon         = REACTION_FACTORY["Burgeon"]
Hyperbloom      = REACTION_FACTORY["Hyperbloom"]


__all__ = ["Reaction", "Amplifying", "Transformative", "Catalyze", "Blooming",
           "Vaporize", "Melt",
           "Frozen", "Overloaded", "ElectroCharged", "Superconduct", "Swirl", "Crystallize", "Shattered", "Burning",
           "Quicken", "Aggravate", "Spread",
           "Bloom", "DendroCore", "Burgeon", "Hyperbloom",
           "REACTION_FACTORY"]
