
from torch import nn

from GTDC.common.model import Model
from GTDC.common.controller import read_char_excel, read_enemy_excel, read_skill_excel, team_generation


class ArtifactModel(nn.Module):
    def __init__(self, char_dir, enemy_dir, skill_dir, char_idx=0):
        super(ArtifactModel, self).__init__()
        self.char_dir = char_dir
        self.enemy_dir = enemy_dir
        self.skill_dir = skill_dir
        self.char_idx = char_idx

        self.char_data = read_char_excel(char_dir)
        enemies = read_enemy_excel(enemy_dir)
        self.enemy = enemies[list(enemies.keys())[0]]

        self.team = team_generation(self.char_data)
        self.skill_df, self.buff_df, self.infusion_df = read_skill_excel(self.team, skill_dir)
        self.model = Model(team=self.team, enemy=self.enemy,
                           skills=self.skill_df,
                           buffs=self.buff_df,
                           infusions=self.infusion_df)

    def change_artifact(self, stats):
        self.char_data[self.char_idx]['artifact']['stats'] = stats
        self.team = team_generation(self.char_data)
        skill_df, buff_df, infusion_df = read_skill_excel(self.team, self.skill_dir)
        self.model = Model(team=self.team, enemy=self.enemy,
                           skills=skill_df,
                           buffs=buff_df,
                           infusions=infusion_df)

    def forward(self, affix):
        self.change_artifact(affix)
        result = self.model.run()[-1]
        return result
