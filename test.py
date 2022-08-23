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
    artifact_stats = torch.tensor([[0., 311., 46.6,
                                    0., 0., 0,
                                    0., 4780., 0,
                                    0, 65, 90., 0., 51.8, 0.,
                                    0., 0.,
                                    0., 0.,
                                    0., 0.,
                                    0., 0.,
                                    0., 0.,
                                    0., 0.,
                                    0., 0.,
                                    0., 0.,
                                    0., 0.]])
    # char_data = [('RaidenShogun', 'EngulfingLightning', 'SeveredFate', 'SeveredFate', artifact_stats)]
    chars_data = read_char_excel()
    # artifact = ArtifactSet(artifact_stats,
    #                        two_set=ARTIFACT_FACTORY['SeveredFate'],
    #                        four_set=ARTIFACT_FACTORY['SeveredFate'])

    enemyies = read_enemy_excel()

    # el = WEAPON_FACTORY['EngulfingLightning']()

    # print(type(artifact.stats))

    # raiden = CHAR_FACTORY['RaidenShogun'](el, artifact)

    team = team_generation(chars_data)

    raiden = team[0]
    weapon = raiden.weapon

    raiden.buff_e.update(90)

    # print(raiden.idx, team.on_field)
    skill_df = pd.DataFrame([(raiden.skill_q, 0, 1.5, None, {}),
                             (raiden.skill_a, 1.5, 2.2, None, {'strike': 1}),
                             (raiden.skill_A, 2.2, 3.5, None, {}),
                             (raiden.skill_a, 3.5, 4.2, None, {'strike': 1}),
                             (raiden.skill_A, 4.2, 5.5, None, {}),
                             (raiden.skill_a, 5.5, 6.2, None, {'strike': 1}),
                             (raiden.skill_A, 6.2, 7.5, None, {}),
                             (raiden.skill_a, 7.5, 8.2, None, {'strike': 1}),
                             (raiden.skill_A, 8.2, 9.5, None, {})],
                            columns=['skill', 'start_time', 'end_time', 'reaction', 'kwarg'])
    buff_df = pd.DataFrame([(raiden.buff_e, 0, 10),
                            (raiden.buff_P, 0, 10),
                            (weapon.buffs[0], 0, 10)], columns=['buff', 'start_time', 'end_time'])
    infusion_df = pd.DataFrame([(raiden.infusion, 0, 10)], columns=['infusion', 'start_time', 'end_time'])

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

