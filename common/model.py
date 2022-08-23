from collections import defaultdict, OrderedDict

import numpy as np
import pandas as pd
import torch
from torch.nn.functional import one_hot

from common.characters.base_char import Character
from common.stats import BasicBuff, ProportionalBuff, Stats, Debuff


class InvalidModel(Exception):
    pass


class InvalidSkillTime(InvalidModel):
    pass


class Team:
    def __init__(self, *chars: Character):
        """

        Pseudo Code:

        for character in team do:
            add permanent_buffs to character
        # consider doing this step in the initialization of the team
        """
        self.chars = chars
        self.on_field = 0
        self.permanent_prop_buffs = tuple([] for i in chars)
        for i, char in enumerate(chars):
            char.weapon.init_char(char)
            char.artifact.init_char(char)
            for b in char.weapon.permanent_buffs + char.artifact.permanent_buffs:

                if isinstance(b, BasicBuff):
                    # print(b)
                    char.stats += b
                elif isinstance(b, ProportionalBuff):
                    # print(b)
                    self.permanent_prop_buffs[i].append(b)
                else:
                    # print(b)
                    # pass
                    raise TypeError
        self.num_chars = len(chars)
        self.stats = Stats(torch.stack(list(map(lambda c: c.stats.data.flatten(), self.chars))))
        self._static_stats = Stats(torch.clone(self.stats.data))
        self._dynamic_stats = Stats(torch.clone(self.stats.data))

    def __getitem__(self, item):
        return self.chars[item]

    def get_stats(self, idx):
        return Stats(self._dynamic_stats[idx])

    def add_basic_buff(self, buff, c_idx):
        # print(self._static_stats)
        # print(len(self._static_stats[c_idx].shape))
        # print(buff)
        self._static_stats[c_idx] += buff.data
        self._dynamic_stats[c_idx] += buff.data

    def add_proportional_buff(self, buff, c_idx):
        buff.load_buff(self._static_stats)
        self._dynamic_stats[c_idx] += buff.data

    def init_stats(self):
        self._static_stats = Stats(torch.clone(self.stats.data))
        self._dynamic_stats = Stats(torch.clone(self.stats.data))


class Model:
    def __init__(self, team, skills, enemy, buffs, infusions):
        """
        Arguments

        team:     Team object
        skills:   {skill: (start_time, end_time, reaction, kwarg={})}
        enemy:    Enemy object
        buffs:    {buff: (start_time, end_time)}
        infusions: {infusion: (start_time, end_time)}

        ===========

        Parameters

        team:           Team object
        enemy:          Enemy object

        skills_data:    pandas DataFrame object storing information of skills
        buffs_data:     pandas DataFrame object storing information of buffs
        infusions_data: pandas DataFrame object storing information of infusions

        time:           the list of the timing
        inv_time:       a dict to map timing to its index

        skills_mat:     time matrix for skills in which one is filled if skill exists on that time, otherwise zero
        buffs_mat:      time matrix for buffs in which one is filled if buff exists on that time, otherwise zero
        infusions_mat:  time matrix for infusions in which one is filled if infusion exists on that time, otherwise zero

        [[0, 1, 1, 1, 0, 0, 0]  this row represents that the skill/buff/infusion starts at time 1 and ends at time 4
         [1, 1, 1, 0, 0, 0, 0]  this row represents that the skill/buff/infusion starts at time 0 and ends at time 3
         [0, 1, 1, 1, 1, 1, 1]] this row represents that the skill/buff/infusion starts at time 1 and ends at time 7

        """
        self.team = team
        self.enemy = enemy

        self.skills_data = skills
        self.buffs_data = buffs
        self.infusions_data = infusions

        self.times = []
        for df in (skills, buffs, infusions):
            for time in['start_time', 'end_time']:
                self.times += df[time].values.tolist()
        self.times = sorted(list(set(self.times)))

        self.inv_time = {time: i for i, time in enumerate(self.times)}
        print()

        self.skills_mat = np.zeros((len(self.skills_data), len(self.times)), dtype=int)

        self.buffs_mat = np.zeros((len(self.buffs_data), len(self.times)), dtype=int)

        self.infusions_mat = np.zeros((len(self.infusions_data), len(self.times)), dtype=int)

        # self.serial = defaultdict(lambda x: (defaultdict(lambda: [x, None, {}]),
        #                                      defaultdict(lambda: x),
        #                                      defaultdict(lambda: x)))

        for i, skill in enumerate(self.skills_data["skill"]):
            skill_start_time, skill_end_time = self.skills_data.loc[i][["start_time", "end_time"]]
            self.skills_mat[i, self.inv_time[skill_start_time]:self.inv_time[skill_end_time]+1] = 1
            # self.serial[skill_start_time][0][skill] = [skill_end_time, reaction, kwarg]

        for i, buff in enumerate(self.buffs_data["buff"]):
            buff_start_time, buff_end_time = self.buffs_data.loc[i][["start_time", "end_time"]]
            self.buffs_mat[i, self.inv_time[buff_start_time]:self.inv_time[buff_end_time]+1] = 1
            # self.serial[buff_start_time][1][buff] = buff_end_time

        for i, infusion in enumerate(self.infusions_data["infusion"]):
            infusion_start_time, infusion_end_time = self.infusions_data.loc[i][["start_time", "end_time"]]
            self.infusions_mat[i, self.inv_time[infusion_start_time]:self.inv_time[infusion_end_time]+1] = 1
            # self.serial[infusion_start_time][2][infusion] = infusion_end_time

        # self.serial = OrderedDict(sorted(self.serial.items(), key=lambda x: x))
        # for time in self.serial:
        #     skills, buffs, infusions = self.serial[time]
        #     self.serial[time] = (OrderedDict(sorted(skills.items(), key=lambda x: skills[x][0])),
        #                          OrderedDict(sorted(buffs.items(), key=lambda x: buffs[x])),
        #                          OrderedDict(sorted(infusions.items(), key=lambda x: infusions[x])))

    def validation(self):
        for i, buff in self.buffs_data['buff'].iteritems():
            # print(self.buffs_data['buff'][i])
            buff_start_time = self.buffs_data['start_time'][i]
            buff_end_time = self.buffs_data['end_time'][i]
            for j, skill in self.skills_data['skill'].iteritems():
                _, skill_start_time, skill_end_time, _, _ = self.skills_data.iloc[j]
                if skill_start_time < buff_start_time < skill_end_time:
                    skill_name = skill.__class__.__name__
                    skill_char_name = skill.char.__class__.__name__
                    buff_name = buff.__class__.__name__
                    buff_char_name = buff.__class__.__name__
                    raise InvalidSkillTime(f"Buff {buff_name} of Character {buff_char_name} started during Skill {skill_name} of Character {skill_char_name}")
                elif skill_start_time < buff_end_time < skill_end_time:
                    skill_name = skill.__class__.__name__
                    skill_char_name = skill.char.__class__.__name__
                    buff_name = buff.__class__.__name__
                    buff_char_name = buff.__class__.__name__
                    raise InvalidSkillTime(f"Buff {buff_name} of Character {buff_char_name} ended during Skill {skill_name} of Character {skill_char_name}")

        for i, infusion in self.infusions_data['infusion'].iteritems():
            infusion_start_time = self.infusions_data['start_time'][i]
            infusion_end_time = self.infusions_data['end_time'][i]
            for j, skill in self.skills_data['skill'].iteritems():
                _, skill_start_time, skill_end_time, _, _ = self.skills_data.iloc[j]
                if skill_start_time < infusion_start_time < skill_end_time:
                    skill_name = skill.__class__.__name__
                    skill_char_name = skill.char.__class__.__name__
                    infusion_name = infusion.__class__.__name__
                    infusion_char_name = infusion.__class__.__name__
                    raise InvalidSkillTime(f"Infusion {infusion_name} of Character {infusion_char_name} started during Skill {skill_name} of Character {skill_char_name}")
                elif skill_start_time < infusion_end_time < skill_end_time:
                    skill_name = skill.__class__.__name__
                    skill_char_name = skill.char.__class__.__name__
                    infusion_name = infusion.__class__.__name__
                    infusion_char_name = infusion.__class__.__name__
                    raise InvalidSkillTime(f"Infusion {infusion_name} of Character {infusion_char_name} ended during Skill {skill_name} of Character {skill_char_name}")

    def run(self):
        t_max = len(self.times)
        total_dmg = torch.zeros(t_max)
        t_last = np.zeros(t_max)
        for start_time in self.times:

            # one hot encoding for the time t
            t = one_hot(torch.tensor(self.inv_time[start_time]), t_max).numpy()

            # skill start at t iff skill is 1 on time t and 0 on time t-1
            valid_skills_mask = (self.skills_mat@t) > 0
            valid_skills_mask *= (self.skills_mat@t_last) == 0
            # print(valid_skills_mask)

            # getting the selected time matrix and data
            valid_skills_mat = self.skills_mat[valid_skills_mask]
            valid_skills_data = self.skills_data.iloc[valid_skills_mask]

            t_last = t

            # create mask for buffs base on their type
            basic_buffs_mask = list(map(lambda y: isinstance(y, BasicBuff), self.buffs_data['buff']))
            proportional_buffs_mask = list(map(lambda y: isinstance(y, ProportionalBuff), self.buffs_data['buff']))
            de_buffs_mask = list(map(lambda y: isinstance(y, Debuff), self.buffs_data['buff']))

            # create mask for buffs and infusions based on time of the skills
            valid_buffs_mask = (self.buffs_mat@valid_skills_mat.T) > 0
            # print(valid_buffs_mask.shape)
            valid_infusions_mask = (self.infusions_mat@valid_skills_mat.T) > 0

            # iterate over the skills start at this time
            for idx, (_, valid_skill) in enumerate(valid_skills_data.iterrows()):
                # print(idx)
                # mask of buffs and infusions for the skill
                valid_buff_mask = valid_buffs_mask[:, idx]
                valid_infusion_mask = valid_infusions_mask[:, idx]

                buffs = (list(self.buffs_data['buff'][valid_buff_mask*basic_buffs_mask]),
                         list(self.buffs_data['buff'][valid_buff_mask*proportional_buffs_mask]),
                         list(self.buffs_data['buff'][valid_buff_mask*de_buffs_mask]))
                infusion = self.infusions_data['infusion'][valid_infusion_mask]
                skill = valid_skill['skill']

                # calculate damages
                # print(infusion)
                dmg = skill.damage(team=self.team, enemy=self.enemy, buffs=buffs, reaction=valid_skill['reaction'],
                                   infusions=infusion, **(valid_skill['kwarg']))
                end_time = valid_skill['end_time']
                # print(self.inv_time[end_time])
                # print(total_dmg)
                # print(total_dmg[(self.inv_time[end_time]):])
                # print(dmg[0])
                total_dmg[(self.inv_time[end_time]):] += dmg[0]

        return total_dmg
