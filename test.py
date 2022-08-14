import numpy as np
import torch
from matplotlib import pyplot as plt

from common.stats import STATS_LENGTH, Buff
from common.model import Team, Model
from common.artifact import ARTIFACT_FACTORY, ArtifactSet
from common.characters import CHAR_FACTORY
from common.enemy import ENEMY_FACTORY
from common.weapon import WEAPON_FACTORY


def team_generation(char_data):
    chars = []
    for data in char_data:
        artifact_set = ArtifactSet(data['artifact']['stats'],
                                   two_set=ARTIFACT_FACTORY[data['artifact']['two_set']],
                                   four_set=ARTIFACT_FACTORY[data['artifact']['four_set']])
        weapon = WEAPON_FACTORY[data['weapon']['name']](data['weapon']['affix'])
        character = CHAR_FACTORY[data['char']['name']](weapon=weapon,
                                                       artifact=artifact_set,
                                                       level=data['char']['level'],
                                                       constellation=data['char']['constellation'])
        chars.append(character)
    team = Team(*chars)
    return team


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
    char_data = [{'char': {'name': 'RaidenShogun',
                           'level': 90,
                           'constellation': 0},
                  'weapon': {'name': 'EngulfingLightning',
                             'affix': 1},
                  'artifact': {'two_set': 'SeveredFate',
                               'four_set': 'SeveredFate',
                               'stats': artifact_stats}}]
    # artifact = ArtifactSet(artifact_stats,
    #                        two_set=ARTIFACT_FACTORY['SeveredFate'],
    #                        four_set=ARTIFACT_FACTORY['SeveredFate'])

    enemy = ENEMY_FACTORY['Hilichurl'](90)

    # el = WEAPON_FACTORY['EngulfingLightning']()

    # print(type(artifact.stats))

    # raiden = CHAR_FACTORY['RaidenShogun'](el, artifact)

    team = team_generation(char_data)

    raiden = team[0]
    weapon = raiden.weapon

    raiden.buff_e.update(90)

    # print(raiden.idx, team.on_field)

    model = Model(team=team, enemy=enemy,
                  skills={raiden.skill_q: (0, 1.5, None, {}),
                          raiden.skill_a: (1.5, 2.2, None, {'strike': 1}),
                          raiden.skill_A: (2.2, 3.5, None, {})},
                  buffs={raiden.buff_e: (0, 10),
                         raiden.buff_P: (0, 10),
                         weapon.buffs[0]: (0, 10)},
                  infusions={raiden.infusion: (0, 10)})

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

