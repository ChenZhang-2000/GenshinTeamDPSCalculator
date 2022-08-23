import numpy as np
import torch
import yaml

from common.stats import STATS_LENGTH, Buff, Stats
from common.model import Team
from common.artifact import ARTIFACT_FACTORY, ArtifactSet
from common.characters import CHAR_FACTORY
from common.enemy import ENEMY_FACTORY
from common.weapon import WEAPON_FACTORY

from common.controller import read_char_excel, team_generation


def main():

    return


if __name__ == "__main__":
    # main()
    chars_data = read_char_excel()
    team_generation(chars_data)
    # print(char_map)

