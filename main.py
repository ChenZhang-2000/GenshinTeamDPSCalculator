import numpy as np

from common.stats import STATS_LENGTH, Buff
from common.artifact import ARTIFACT_FACTORY, ArtifactSet
from common.characters import CHAR_FACTORY
from common.enemy import ENEMY_FACTORY
from common.weapon import WEAPON_FACTORY


def main():

    return


if __name__ == "__main__":
    # main()
    print(CHAR_FACTORY['RaidenShogun'](WEAPON_FACTORY['EngulfingLightning'](),
                                       ENEMY_FACTORY['Hilichurl'](),
                                       ArtifactSet(two_set=ARTIFACT_FACTORY['SeveredFate'],
                                                   four_set=ARTIFACT_FACTORY['SeveredFate'])
                                       ).stats.data)

