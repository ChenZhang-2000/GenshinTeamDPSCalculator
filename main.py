import numpy as np
import torch
import yaml
import matplotlib.pyplot as plt

from GTDC.common.stats import STATS_LENGTH, Buff, Stats
from GTDC.common.model import Team, Model
from GTDC.common.artifact import ARTIFACT_FACTORY, ArtifactSet
from GTDC.common.characters import CHAR_FACTORY
from GTDC.common.enemy import ENEMY_FACTORY
from GTDC.common.weapon import WEAPON_FACTORY

from GTDC.common.controller import read_char_excel, read_enemy_excel, team_generation, read_skill_excel, terminal_ui


def main():

    return


if __name__ == "__main__":
    # main()
    damage_result, models = terminal_ui()
    for i in range(len(models)):
        total_dmg = damage_result[i]
        model = models[i]
        # print(model._dynamic_stats)
        print(total_dmg[-1])
        plt.plot(model.times, total_dmg)
        plt.xlabel('Time')
        plt.ylabel('DMG')
        plt.show()

