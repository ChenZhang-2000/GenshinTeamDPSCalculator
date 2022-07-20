import numpy as np
import torch

from common.characters.base_char import Character


class Team:
    def __init__(self, *chars: Character):
        self.chars = chars
        self.num_chars = len(chars)

    def __getitem__(self, item):
        return self.chars[item]

    def stats(self):
        return torch.vstack(list(map(lambda c: c.data, self.chars)))


class Model:
    def __init__(self, chars, skills, skill_args, buffs,
                 time: np.array, on_field: np.array, action: (np.array, np.array),
                 reaction: np.array, buffs_coverage: (np.array, np.array)):
        """
        data: 2d numpy array with 8 x number of the timestamps
            example:
            time stamp         1  2  3  4  5  6       # time argument

            on field char      0  2  3  3  1  0       # on_field argument

            0: RaidenShogun    2  NaN  NaN  NaN  NaN  0       # skill argument
            1: KujouSara       NaN  NaN  NaN  0  3  NaN
            2: Bennett         NaN  4  0  NaN  NaN  0
            3: Kazuha          NaN  NaN  3  4  0  NaN

            4: Reaction        0  1  2  2  0  1       # reaction argument

            5: Kazuha          0  0  1  1  1  1       # buffs argument


            the first row is the time stamp in second
            the second row is the index of the character that is on field
            the third to the sixth row is the skills that character used
        """
        self.chars = chars
        '''
        [RaidenShogun, KujouSara, Bennett, Kazuha]
        '''
        self.skills = skills
        '''
        [[RaidenShogun.a, RaidenShogun.A, RaidenShogun.e], 
         [KujouSara.a, KujouSara.A, KujouSara.e], 
         [Bennett.a, Bennett.A, Bennett.e], 
         [Kazuha.a, Kazuha.A, Kazuha.e]]
        '''
        self.skill_args = skill_args
        '''
        [[[element], [], []], 
         [[element], [], []], 
         [[element], [], []], 
         [[element], [], []]]
        '''
        self.buffs = buffs
        '''
        [[RaidenShogun.buff_p, RaidenShogun.buff_P], 
         [KujouSara.buff_p, KujouSara.buff_P], 
         [Bennett.buff_p, Bennett.buff_P], 
         [Kazuha.buff_p, Kazuha.buff_P]]
        '''

        self.time = time
        self.on_field = on_field

        self.action_owner, self.action = action
        self.buffs_owner, self.buffs_coverage = buffs_coverage
        self.reaction = reaction

    # def mask(self):
    #     mask = np.zeros(self.skills.shape)
    #     for char in self.build_map:
    #         char_skills = self.skills[char, :]
    #         char_mask = np.zeros(char_skills.shape)
    #         for skill in self.build_map[char]['skills']:
    #             skill_mask = char_skills == skill
    #             skill_mask / np.sum(skill_mask)
    #             char_mask += (skill_mask / np.sum(skill_mask))
    #         mask[char] += char_mask
    #     return mask

    def calculate(self):
        total_dmg = 0.
        for t in range(self.time.shape[-1]):
            for c in range(4):
                skill_idx = self.action[c, t]
                if np.isnan(skill_idx):
                    dmg = 0
                else:
                    buff_idx = self.buffs_coverage[:, t]
                    buffs = (self.buffs[self.buffs_owner[b]][buff_idx[b]]
                             for b in range(buff_idx.shape[0])
                             if not np.isnan(buff_idx[b]))

                    dmg = self.skills[c][skill_idx](
                        *(self.skill_args[c][skill_idx]),
                        buff=buffs)
                total_dmg += dmg
        return total_dmg
