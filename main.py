import numpy as np
import torch
import yaml
import matplotlib.pyplot as plt

from common.stats import STATS_LENGTH, Buff, Stats
from common.model import Team, Model
from common.artifact import ARTIFACT_FACTORY, ArtifactSet
from common.characters import CHAR_FACTORY
from common.enemy import ENEMY_FACTORY
from common.weapon import WEAPON_FACTORY

from common.controller import read_char_excel, read_enemy_excel, team_generation, read_skill_excel, terminal_ui


def main():

    return


if __name__ == "__main__":
    # main()
    damage_result = terminal_ui()
    # print(total_dmg[-1])
    # plt.plot(model.times, total_dmg)
    # plt.xlabel('Time')
    # plt.ylabel('DMG')
    # plt.show()

