import numpy as np
import torch
import yaml
import matplotlib.pyplot as plt
from matplotlib import font_manager

from GTDC.common.stats import STATS_LENGTH, Buff, Stats
from GTDC.common.model import Team, Model
from GTDC.common.artifact import ARTIFACT_FACTORY, ArtifactSet
from GTDC.common.characters import CHAR_FACTORY
from GTDC.common.enemy import ENEMY_FACTORY
from GTDC.common.weapon import WEAPON_FACTORY

from GTDC.common.controller import read_char_excel, read_enemy_excel, team_generation, read_skill_excel, terminal_ui

fontP = font_manager.FontProperties()
fontP.set_family('SimHei')
fontP.set_size(14)


def main():

    return


if __name__ == "__main__":
    # main()
    damage_result, models_x_enemies, ws_names, enemy_names = terminal_ui()
    for i, enemy_name in enumerate(enemy_names):
        for j in range(len(models_x_enemies[0])):
            damage_stats = damage_result[i][j]
            total_dmg = damage_stats.output("time")
            # print(total_dmg[-1])
            plt.plot(total_dmg[0], total_dmg[1])
            plt.xlabel('Time')
            plt.ylabel('DMG')
        plt.title(f"Enemy: {enemy_name}")
        plt.legend(ws_names, prop=fontP)
        plt.show()

