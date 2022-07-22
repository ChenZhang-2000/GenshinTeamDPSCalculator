import numpy as np
import torch

from common.stats import STATS_LENGTH, Buff
from common.model import Team
from common.artifact import ARTIFACT_FACTORY, ArtifactSet
from common.characters import CHAR_FACTORY
from common.enemy import ENEMY_FACTORY
from common.weapon import WEAPON_FACTORY


if __name__ == "__main__":
    # main()
    artifact = ArtifactSet(two_set=ARTIFACT_FACTORY['SeveredFate'],
                           four_set=ARTIFACT_FACTORY['SeveredFate'])
    artifact.set_stats(torch.tensor([[0., 311+39., 4.1+46.6, 0., 21+16+21., 7.3+16, 0., 4780., 5.8, 42., 66.1,
                                      80., 0., 66.7, 0., 0., 0., 0., 0., 0., 0., 0.,
                                      0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]]))

    raiden = CHAR_FACTORY['RaidenShogun'](WEAPON_FACTORY['EngulfingLightning'](),
                                          ENEMY_FACTORY['Hilichurl'](),
                                          artifact)

    team = Team(raiden)

    # print(raiden.stats.data)

