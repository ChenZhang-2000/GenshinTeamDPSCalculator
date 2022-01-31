from collections import defaultdict


class Stat:
    """
    Base class for object having numerical datas with base attack, attack, cr, cd, and damage bonus
    """
    def __init__(self, batk, atk=0., critical_rate=0., critical_dmg=0., dmg_bonus=0.):
        self.batk = float(batk)
        self.atk = float(atk)
        self.critical_rate = float(critical_rate)
        self.critical_dmg = float(critical_dmg)
        self.dmg_bonus = float(dmg_bonus)

    def set_batk(self, batk):
        self.batk = batk

    def set_atk(self, atk):
        self.atk = atk

    def set_cr(self, critical_rate):
        self.critical_rate = critical_rate

    def set_cd(self, critical_dmg):
        self.critical_dmg = critical_dmg

    def set_db(self, dmg_bonus):
        self.dmg_bonus = dmg_bonus

    def print_info(self):
        print(self.batk, self.atk, self.critical_rate, self.critical_dmg, self.dmg_bonus)


class Enemy:
    """
    Class for Enemies
    """
    param_num = 11

    def __init__(self, name, level=100, defence=500, dmg_red=0, *args):
        """
        Params:
            enemy name,
            enemy level,
            enemy defence (usually 500),
            enemy's damage reduction (usually zero),
            Pyro Resistence,
            Hydro Resistence,
            Electro Resistence,
            Anemo Resistence,
            Cryo Resistence,
            Geo Resistence,
            Physical Resistence
        """
        self.name = name
        self.level = level
        self.defence = defence
        self.dmg_red = dmg_red
        elements = ['火', '水', '雷', '风', '冰', '岩', '物']
        self.resistence = {elements[i]: float(args[i]) for i in range(7)}

    def get_printable_info(self):
        return [self.name, self.level, self.defence, self.dmg_red] + \
               [self.resistence[element] for element in ['火', '水', '雷', '风', '冰', '岩', '物']]

    def get_info(self):
        return self.get_printable_info()

    def set_name(self, value):
        self.name = value

    def set_level(self, value):
        self.level = value

    def set_defence(self, value):
        self.defence = value

    def set_dmg_red(self, value):
        self.dmg_red = value

    def set_resistence(self, element, value):
        self.resistence[element] = value


class Character(Stat):
    """
    Class for character
    """
    param_num = 6

    def __init__(self, name, batk, atk=0., critical_rate=0., critical_dmg=0., dmg_bonus=0.):
        """
        Params:
            character name,
            base attack,
            attack,
            critical rate,
            critical damage,
            damage bonus
        """
        self.name = name
        super(Character, self).__init__(batk, atk, critical_rate, critical_dmg, dmg_bonus)

    def get_printable_info(self):
        return  #  [self.name, self.batk, round(self.atk, 2), round(self.critical_rate, 2),
                #   round(self.critical_dmg, 2), round(self.dmg_bonus, 2)]

    def get_info(self):
        return #  [self.name, self.batk, self.atk, self.critical_rate, self.critical_dmg, self.dmg_bonus]

    def print_info(self):
        return
        # print(self.name, self.batk, self.atk, self.critical_rate, self.critical_dmg, self.dmg_bonus)

    def skill_a(self):
        return

    def skill_A(self):
        return

    def skill_e(self):
        return

    def skill_E(self):
        return

    def skill_q(self):
        return

    def skill_Q(self):
        return

    def skill_p(self):
        return

    def skill_P(self):
        return

    def buff_a(self):
        return

    def buff_A(self):
        return

    def buff_e(self):
        return

    def buff_E(self):
        return

    def buff_q(self):
        return

    def buff_Q(self):
        return

    def buff_p(self):
        return

    def buff_P(self):
        return


class Skill(Stat):
    """
    Class for skill
    """
    def __init__(self, name, character: Character, dmg_multiplier, patk, atk=0.,
                 critical_rate=0., critical_dmg=0., dmg_bonus=0.,
                 res_reduction=0., def_reduction=0., independent_multiplier=0., element_type="物"):
        """
        Params:
            skill name,
            character,
            damage multiplier,
            percentage attack,
            fixed value attack,
            critical rate,
            critical damage,
            damage bonus,
            resistence reduction,
            defence reduction,
            independent multiplier,
            element type
        """
        self.name = name
        self.char = character
        self.dmgm = dmg_multiplier
        self.patk = patk
        self.buff_atk = atk
        self.buff_cr = critical_rate
        self.buff_cd = critical_dmg
        self.buff_db = dmg_bonus
        super(Skill, self).__init__(self.char.batk,
                                    self.char.atk + self.buff_atk + self.char.batk * self.patk/100,
                                    self.char.critical_rate + critical_rate,
                                    self.char.critical_dmg + critical_dmg,
                                    self.char.dmg_bonus + dmg_bonus)
        self.res_red = res_reduction
        self.def_red = def_reduction
        self.im = independent_multiplier
        self.element = element_type

    def same_name(self, name):
        return name == self.name

    def get_info(self):
        return [self.name, self.char.name, self.dmgm, self.patk, self.buff_atk, self.buff_cr, self.buff_cd,
                self.buff_db, self.res_red, self.def_red, self.im, self.element]

    def get_printable_info(self):
        return [self.name, self.char.name, round(self.dmgm, 2), round(self.patk, 2), round(self.buff_atk, 2),
                round(self.buff_cr, 2), round(self.buff_cd, 2), round(self.buff_db, 2), round(self.res_red, 2),
                round(self.def_red, 2), round(self.im, 2), self.element]

    def print_info(self):
        print(self.name, self.char.name, self.dmgm, self.patk, self.buff_atk, self.buff_cr, self.buff_cd,
              self.buff_db, self.res_red, self.def_red, self.im, self.element)

    def calc_dmg(self, enemy):
        """
        This method will first update the information of the total values by calling father class Skill.
        Then it'll calculate the expectation of critical strikes, resistence multiplier, and defence multiplier.
        In the last it'll calculate and return the damages.

        :param enemy: class Enemy
        :return: a float point number of the mathematical expectation of damages caused by this skill
        """
        self.atk = self.char.atk + self.buff_atk + self.char.batk * self.patk/100
        self.critical_rate = self.char.critical_rate + self.buff_cr
        self.critical_dmg = self.char.critical_dmg + self.buff_cd
        self.dmg_bonus = self.char.dmg_bonus + self.buff_db

        if self.critical_rate <= 100:
            cd = (1 + self.critical_rate * self.critical_dmg / 10000)
        else:
            cd = 1 + self.critical_dmg/100

        res = enemy.resistence[self.element]

        if res < 0:
            rs = ((1-res/100) + self.res_red/100 - 1) / 2 + 1
        else:
            original_res = res/100-self.res_red/100
            if original_res < 0:
                rs = -original_res / 2 + 1
            elif original_res >= 0.75:
                rs = 1 / (1 + 4 * original_res)
            else:
                rs = 1 - original_res

        dr = (5*90+500)/(enemy.defence*(1+enemy.level/100)*(1-self.def_red/100)+5*90+500)

        # print(self.dmgm, self.atk, self.critical_rate, self.critical_dmg, self.dmg_bonus, rs, dr)

        dmg = self.atk * self.dmgm/100 * cd * (1+self.dmg_bonus/100) * rs * (1+self.im/100) * dr * (1-enemy.dmg_red/100)
        return dmg

    def set_name(self, value):
        self.name = value

    def set_char(self, value):
        self.char = value

    def set_dmgm(self, value):
        self.dmgm = value

    def set_patk(self, value):
        self.patk = value

    def set_batk(self, value):
        self.buff_atk = value

    def set_bcr(self, value):
        self.buff_cr = value

    def set_bcd(self, value):
        self.buff_cd = value

    def set_bdb(self, value):
        self.buff_db = value

    def set_rr(self, value):
        self.res_red = value

    def set_dr(self, value):
        self.def_red = value

    def set_im(self, value):
        self.im = value

    def set_element(self, element):
        self.element = element

    def buff_dmg_multiplier(self, value):
        self.dmgm += value

    def buff_patk(self, value):
        self.patk += value
        self.atk += self.char.batk * value/100

    def buff_attack(self, value):
        self.buff_atk += value
        self.atk += value

    def buff_critical_rate(self, value):
        self.buff_cr += value
        self.critical_rate += value

    def buff_critical_dmg(self, value):
        self.buff_cd += value
        self.critical_dmg += value

    def buff_dmg_bonus(self, value):
        self.buff_db += value
        self.dmg_bonus += value

    def buff_res_reduction(self, value):
        self.res_red += value

    def buff_def_reduction(self, value):
        self.def_red += value

    def buff_independent_multiplier(self, value):
        self.im += value


class Team:
    """
    This is a class of a team, with a bunch of skills in it
    """
    def __init__(self, name, remark, *skills, time=1):
        """
        :param name: name of the TEAM
        :param remark: remark for the TEAM
        :param skills: the skills in the time
        :param time: time costs for the team to finish a round of skills
        """
        self.name = name
        self.remark = remark
        self.time = time
        self._skills = [skill for skill in skills]
        self.idx_name = defaultdict(lambda: [])
        for i, skill in enumerate(skills):
            self.idx_name[skill.name].append(i)

    def _idx_error(self, idx, keys):
        """
        This method will raise Index Error when there is invalid index
        :param idx: index
        :param keys: keys that exists
        """
        if idx not in keys:
            raise IndexError(f"Index {idx} doesn't exist")

    def __len__(self): return len(self._skills)

    def __getitem__(self, idx):
        """
        This class will find and return the target skill(s)
        :param idx: index could be string, integer, or list/tuple of string and integers.
        :return:
        """
        if isinstance(idx, str):
            self._idx_error(idx, self.idx_name.keys())
            return self[self.idx_name[idx]]

        elif isinstance(idx, list) or isinstance(idx, tuple):
            if len(idx) == 0:
                raise IndexError(f"Invalid index: {idx}")
            target_skills = []
            for i in idx:
                target_skills.append(self.__getitem__(i))
            return target_skills

        elif isinstance(idx, int):
            self._idx_error(idx, list(range(self.__len__())))
            return self._skills[idx]

        else:
            raise TypeError(f"Invalid index type: {type(idx)}")

    def __delitem__(self, idx):
        """
        This class will find and delete the target skill(s)
        :param idx: index could be string, integer, or list/tuple of string and integers (can't be mixed).
        :return:
        """
        if isinstance(idx, str):
            self._idx_error(idx, self.idx_name.keys())
            self.__delitem__(self.idx_name[idx])
            # del self.idx_name[idx]

        elif isinstance(idx, list) or isinstance(idx, tuple):
            if len(idx) == 0:
                raise IndexError(f"Invalid index: {idx}")
            target_skills = []
            if isinstance(idx[0], str):
                sort_key = lambda x: self.idx_name[idx]
                keys = self.idx_name.keys()
            else:
                sort_key = lambda x: x
                keys = list(range(self.__len__()))
            for i in sorted(idx, key=sort_key, reverse=True):
                self._idx_error(idx, keys)
                self._skills.pop(i)
            return target_skills

        elif isinstance(idx, int):
            self._idx_error(idx, list(range(self.__len__())))
            del self.idx_name[self._skills[idx].name]
            self._skills.pop(idx)

        else:
            raise TypeError(f"Invalid index type: {type(idx)}")

    def __setitem__(self, idx, skill):
        """
        This class will find and set the target skill(s) to the target value
        :param idx: index could be string, integer, or list/tuple of string and integers
        :return:
        """
        if not isinstance(skill, Skill):
            raise TypeError(f"Invalid skill type: {type(skill)}")

        if isinstance(idx, str):
            if skill.name != idx and skill.name in self.idx_name.keys():
                raise KeyError(f"Skill's name {skill.name} is not as same as the key {idx} but exists in team already")
            self._idx_error(idx, self.idx_name.keys())
            int_idx = self.idx_name[idx]
            self._skills[int_idx] = skill
            del self.idx_name[idx]
            self.idx_name[skill.name] = int_idx

        elif isinstance(idx, int):
            self._idx_error(idx, list(range(self.__len__())))
            self._skills[idx] = skill

        else:
            raise TypeError(f"Invalid index type: {type(idx)}")

    def insert(self, idx, skill):
        """
        This class will insert a skill at certain index
        :param idx: index could be string, integer
        :return:
        """
        if not isinstance(skill, Skill):
            raise TypeError(f"Invalid skill type: {type(skill)}")

        if isinstance(idx, str):
            if idx in self.idx_name.keys():
                int_idx = self.idx_name[idx]
                self._skills.insert(int_idx, skill)
                self.idx_name = {skill.name: i for i, skill in enumerate(self._skills)}
            else:
                if idx != skill.name:
                    raise KeyError(f'Index {idx} is not found and different from {skill.name}')
                self.idx_name[skill.name] = self.__len__()
                self._skills.append(skill)
                self.idx_name[skill.name] = self.__len__()

        elif isinstance(idx, int):
            self._idx_error(idx, list(range(self.__len__()+1)))
            self._skills.insert(idx, skill)

        else:
            raise TypeError(f"Invalid index type: {type(idx)}")

    def append(self, skill):
        if not isinstance(skill, Skill):
            raise TypeError(f"Invalid skill type: {type(skill)}")
        self._skills.append(skill)
        self.idx_name[skill.name] = self.__len__()

    def __iter__(self):
        for skill in self._skills:
            yield skill

    def skill_names(self):
        return self.idx_name.keys()

    def skills(self):
        return self._skills

    def _calc_dmg(self, enemy):
        """
        This method will calculate and return the damages dealt by the team
        :param enemy: enemy being attacked by the team
        :return:
        """
        dmg = 0
        for skill in self._skills:
            dmg += skill.calc_dmg(enemy)
        return dmg

    def calc_dmg(self, enemy):
        """
        This method will return the dictionary with key being team name and value being damages
        :param enemy: enemy being attacked by the team
        :return:
        """
        if isinstance(enemy, Enemy):
            return {self.name: self._calc_dmg(enemy)}
        else:
            raise TypeError(f"Wrong enemy type {type(enemy)}")

    def _calc_chars_dmg(self, enemy):
        """
        This method will calculate and return the damages dealt by each characters
        :param enemy: enemy being attacked by the team
        :return:
        """
        dmg = 0
        chars_dmg = defaultdict(lambda: 0)
        for skill in self._skills:
            dmg += skill.calc_dmg(enemy)
            chars_dmg[skill.char.name] += skill.calc_dmg(enemy)
        chars_dmg['总伤'] = dmg
        return chars_dmg

    def calc_chars_dmg(self, enemy):
        """
        This method will return the dictionary with key being team name and value being damages dealt by each characters
        :param enemy: enemy being attacked by the team
        :return:
        """
        if isinstance(enemy, Enemy):
            return {self.name: self._calc_chars_dmg(enemy)}
        else:
            raise TypeError(f"Wrong enemy type {type(enemy)}")

