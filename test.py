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
    artifact = ArtifactSet(torch.tensor([[0., 311., 46.6,
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
                                          0., 0.]]),
                           two_set=ARTIFACT_FACTORY['SeveredFate'],
                           four_set=ARTIFACT_FACTORY['SeveredFate'])

    hilichurl = ENEMY_FACTORY['Hilichurl'](90)

    el = WEAPON_FACTORY['EngulfingLightning']()

    raiden = CHAR_FACTORY['RaidenShogun'](el, hilichurl, artifact)

    team = Team(raiden)

    raiden.buff_e.update(90)

    # print(raiden.idx, team.on_field)

    # print(raiden.infusion.skill_types_from)
    q_dmg = raiden.skill_q.damage(team,
                                  hilichurl,
                                  ([raiden.buff_e] + el.buffs,
                                   [raiden.buff_P],
                                   []),
                                  None,
                                  raiden.infusion).item()
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
    print(f"Q Damage: {q_dmg}")
    # print(f"Total Damage: {q_dmg + a_dmg*5 + A_dmg*5}")

    # print(raiden.stats.data)

