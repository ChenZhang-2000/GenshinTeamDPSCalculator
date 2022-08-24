import numpy as np
import pandas as pd
import torch
from matplotlib import pyplot as plt

from common.stats import STATS_LENGTH, Buff
from common.model import Team, Model
from common.artifact import ARTIFACT_FACTORY, ArtifactSet
from common.characters import CHAR_FACTORY
from common.enemy import ENEMY_FACTORY
from common.weapon import WEAPON_FACTORY
from common.controller import team_generation, read_char_excel, read_enemy_excel


if __name__ == "__main__":
    # main()
    chars_data = read_char_excel()
    enemyies = read_enemy_excel()
    team = team_generation(chars_data)

    raiden = team[0]
    weapon = raiden.weapon

    raiden.buff_e.update(90)

    # print(raiden.idx, team.on_field)
    skill_df = pd.DataFrame([(raiden.skill_q, 1, 3, None, {}),
                             (raiden.skill_a, 3, 3.5, None, {}),
                             (raiden.skill_A, 3.5, 4.5, None, {}),
                             (raiden.skill_a, 4.5, 5, None, {}),
                             (raiden.skill_A, 5, 6., None, {}),
                             (raiden.skill_a, 6., 6.5, None, {}),
                             (raiden.skill_A, 6.5, 7.5, None, {}),
                             (raiden.skill_a, 7.5, 8, None, {}),
                             (raiden.skill_A, 8., 9., None, {}),
                             (raiden.skill_a, 9, 9.5, None, {}),
                             (raiden.skill_A, 9.5, 10.5, None, {}),
                             (raiden.skill_e, 0, 1, None, {}),
                             (raiden.skill_e, 1, 3, None, {}),
                             (raiden.skill_e, 3, 3.5, None, {}),
                             (raiden.skill_e, 3.5, 4.5, None, {}),
                             (raiden.skill_e, 5, 6, None, {}),
                             (raiden.skill_e, 6.5, 7.5, None, {}),
                             (raiden.skill_e, 8, 9, None, {}),
                             (raiden.skill_e, 9.5, 10.5, None, {})
                             ],
                            columns=['skill', 'start_time', 'end_time', 'reaction', 'kwarg'])
    buff_df = pd.DataFrame([(raiden.buff_e, 0, 10.5),
                            (raiden.buff_P, 0, 10.5),
                            (weapon.buffs[0], 0, 10.5)], columns=['buff', 'start_time', 'end_time'])
    infusion_df = pd.DataFrame([(raiden.infusion, 0, 10.5)], columns=['infusion', 'start_time', 'end_time'])

    print(buff_df)

    model = Model(team=team, enemy=enemyies['Hilichurl'],
                  skills=skill_df,
                  buffs=buff_df,
                  infusions=infusion_df)

    model.validation()
    total_dmg = model.run()
    plt.plot(model.times, total_dmg)
    plt.show()

    # print(raiden.infusion.skill_types_from)
    # q_dmg = raiden.skill_q.damage(team,
    #                               enemy,
    #                               ([raiden.buff_e] + weapon.buffs,
    #                                [raiden.buff_P],
    #                                []),
    #                               None,
    #                               raiden.infusion).item()
    # a_dmg = raiden.skill_a.damage(team,
    #                               hilichurl,
    #                               ([raiden.buff_e] + el.buffs,
    #                                [raiden.buff_P],
    #                                []),
    #                               None,
    #                               raiden.infusion,
    #                               strike=1).item()
    # A_dmg = raiden.skill_A.damage(team,
    #                               hilichurl,
    #                               ([raiden.buff_e] + el.buffs,
    #                                [raiden.buff_P],
    #                                []),
    #                               None,
    #                               raiden.infusion).item()
    # print(f"Q Damage: {q_dmg}")
    # print(f"Total Damage: {q_dmg + a_dmg*5 + A_dmg*5}")

    # print(raiden.stats.data)

