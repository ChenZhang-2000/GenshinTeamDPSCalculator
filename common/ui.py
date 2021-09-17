from typing import Dict, Any, Callable

from collections import defaultdict
from prettytable import PrettyTable
from openpyxl.workbook import Workbook

from common import exl_operation as ExcelOperation, stats
import re


class InvalidModException(Exception):
    """
    Exception throwed when there is invalid mode
    """
    pass


def main_loop(chars, enemies, teams):
    while True:
        instruction = input("请输入操作指令（修改角色信息/修改敌人信息/修改技能循环/计算队伍输出/导出队伍输出/quit）：")
        # print("test")
        if instruction == "修改角色信息":
            # print("test")
            modify_stats('char', chars)
        elif instruction == '修改敌人信息':
            modify_stats('enemy', enemies)
        elif instruction == '修改技能循环':
            modify_teams(teams, chars)
        elif instruction == '计算队伍输出':
            dmg_data = calculate_dmg(enemies, teams)
            print_calculated_dmg(dmg_data, teams)
        elif instruction == '导出队伍输出':
            get_output(enemies, teams)
        elif instruction == 'quit':
            break
        else:
            print("无效的操作指令，请重新输入")


_CHARS_PARAMS: Dict[str, Callable[[stats.Character, str or int or float], None]]\
              = {"角色名称": lambda x, value: x.set_name(value),
                 "基础攻击": lambda x, value: x.set_batk(value),
                 "攻击力": lambda x, value: x.set_atk(value),
                 "暴击率": lambda x, value: x.set_cr(value),
                 "暴击伤害": lambda x, value: x.set_cd(value),
                 "常驻增伤": lambda x, value: x.set_db(value)}

_ENEMY_PARAMS: Dict[str, Callable[[stats.Enemy, str or int or float], None]]\
              = {"敌方名称": lambda x, value: x.set_name(value),
                 "敌方等级": lambda x, value: x.set_level(value),
                 "防御": lambda x, value: x.set_defence(value),
                 "减伤": lambda x, value: x.set_dmg_red(value),
                 "火抗": lambda x, value: x.set_resistence('火', value),
                 "水抗": lambda x, value: x.set_resistence('水', value),
                 "雷抗": lambda x, value: x.set_resistence('雷', value),
                 "风抗": lambda x, value: x.set_resistence('风', value),
                 "冰抗": lambda x, value: x.set_resistence('冰', value),
                 "岩抗": lambda x, value: x.set_resistence('岩', value),
                 "物抗": lambda x, value: x.set_resistence('物', value)}

_TEAM_PARAMS: Dict[str, Callable[[stats.Skill, str or int or float], Any]]\
              = {"技能名称": lambda x, value: x.set_name(value),
                 "释放角色": lambda x, value: x.set_char(value),
                 "技能倍率": lambda x, value: x.set_dmgm(value),
                 "百分比攻击": lambda x, value: x.set_patk(value),
                 "固定攻击": lambda x, value: x.set_batk(value),
                 "暴击率": lambda x, value: x.set_bcr(value),
                 "暴击伤害": lambda x, value: x.set_bcd(value),
                 "增伤": lambda x, value: x.set_bdb(value),
                 "减抗": lambda x, value: x.set_rr(value),
                 "减防": lambda x, value: x.set_dr(value),
                 "独立乘区": lambda x, value: x.set_im(value),
                 "元素": lambda x, value: x.set_element(value)}

_BUFF_PARAMS: Dict[str, Callable[[stats.Skill, str or int or float], None]]\
              = {"技能倍率": lambda x, value: x.buff_dmg_multiplier(value),
                 "百分比攻击": lambda x, value: x.buff_patk(value),
                 "固定攻击": lambda x, value: x.buff_attack(value),
                 "暴击率": lambda x, value: x.buff_critical_rate(value),
                 "暴击伤害": lambda x, value: x.buff_critical_dmg(value),
                 "增伤": lambda x, value: x.buff_dmg_bonus(value),
                 "减抗": lambda x, value: x.buff_res_reduction(value),
                 "减防": lambda x, value: x.buff_def_reduction(value),
                 "独立乘区": lambda x, value: x.buff_independent_multiplier(value)}


def _print_table(target_name, headers, data):
    """
    Print the table of the data given
    :param target_name: the name of the data
    :param headers: the headers of the data
    :param data: the data itself
    :return:
    """
    print(f"当前{target_name}信息表格")
    table = PrettyTable(headers)
    for obj in data:
        table.add_row(obj.get_printable_info())
    print(table)


def _change_value(mode, data, chars=None):
    """
    This function will create user interface follows the following logics:

        present the current data
        take input of the target object (such as character, enemy, or skill)
            take input of the parameters' name (such as attack, critical rate, critical damage, etc.)
                take input of the value to be change
                change value
            present the current data

    :param mode: the mode of the function, decided by the type of the data to be change
    :param data: the data to be change
    :param chars: the characters' info (only used for changing team)
    """
    if mode == 'char':
        global _CHARS_PARAMS
        params_map = _CHARS_PARAMS
        target_name = '角色'
    elif mode == 'enemy':
        global _ENEMY_PARAMS
        params_map = _ENEMY_PARAMS
        target_name = '敌方'
    elif mode == 'team':
        global _TEAM_PARAMS
        params_map = _TEAM_PARAMS
        target_name = '技能'
    else:
        raise InvalidModException()

    name_obj_map = {obj.name: data[idx] for idx, obj in enumerate(data)}

    while True:

        _print_table(target_name, params_map.keys(), data)

        obj_name = input(f"请输入要修改的{target_name}名称：")
        if obj_name in name_obj_map.keys():
            while True:
                param_name = input("请输入要修改的参数名称（输入quit结束修改）：")
                if param_name in params_map.keys():
                    value = input("请输入要修改的参数数值：")
                    if mode == "team" and param_name == '释放角色':
                        name_char_map = {char.name: chars[idx] for idx, char in enumerate(chars)}
                        if value in name_char_map.keys():
                            params_map[param_name](name_obj_map[obj_name], name_char_map[value])
                        else:
                            print("无效的释放角色，请重新输入")
                            print()
                    else:
                        params_map[param_name](name_obj_map[obj_name], value)
                elif param_name == 'quit':
                    break
                else:
                    print("无效的参数名称，请重新输入")
                    print()
                _print_table(target_name, params_map.keys(), data)
            break
        else:
            print(f"无效的{target_name}名称，请重新输入")
            print()


def _add_new(mode, data, chars=None):
    """
    This function will create user interface follows the following logics:

        present the current data
        take input of the values of the object to be added
        add object

    :param mode: the mode of the function, decided by the type of the data to be change
    :param data: the data to be change
    :param chars: the characters' info (only used for changing team)
    """
    if mode == 'char':
        global _CHARS_PARAMS
        params_map = _CHARS_PARAMS
        target_name = '角色'
        params = "基础攻击/攻击力/暴击率/暴击伤害/常驻增伤"
        param_num = 6
        OBJ = stats.Character
    elif mode == 'enemy':
        global _ENEMY_PARAMS
        params_map = _ENEMY_PARAMS
        target_name = '敌方'
        params = "敌人等级/防御/减伤/火抗/水抗/雷抗/风抗/冰抗/岩抗/物抗"
        param_num = 11
        OBJ = stats.Enemy
    elif mode == 'team':
        global _TEAM_PARAMS
        params_map = _TEAM_PARAMS
        target_name = '技能'
        params = "释放角色/技能倍率/百分比攻击/固定攻击/暴击率/暴击伤害/增伤/减抗/减防/独立乘区/元素"
        param_num = 12
        OBJ = stats.Skill
    else:
        raise InvalidModException()

    while True:
        _print_table(target_name, params_map.keys(), data)
        print(f"请输入要新增的{target_name}信息，格式：\n{target_name}名称/{params}")
        info = input()
        try:
            informations = info.split('/')
            if len(informations) != param_num:
                raise
            if mode == 'team':
                name_idx_map = {char.name: idx for idx, char in enumerate(chars)}
                informations[1] = chars[name_idx_map[informations[1]]]
            new_char = OBJ(*informations)
            data.append(new_char)
            break
        except:
            print(f"无效的{target_name}信息，请重新输入")
            print()


def _delete(mode, data, chars=None):
    """
    This function will create user interface follows the following logics:

        present the current data
        take input of the name of the object to be deleted
        delete object

    :param mode: the mode of the function, decided by the type of the data to be change
    :param data: the data to be change
    :param chars: the characters' info (only used for changing team)
    """
    if mode == 'char':
        global _CHARS_PARAMS
        params_map = _CHARS_PARAMS
        target_name = '角色'
    elif mode == 'enemy':
        global _ENEMY_PARAMS
        params_map = _ENEMY_PARAMS
        target_name = '敌方'
    elif mode == 'team':
        global _TEAM_PARAMS
        params_map = _TEAM_PARAMS
        target_name = '技能'
    else:
        raise InvalidModException()

    name_idx_map = {obj.name: idx for idx, obj in enumerate(data)}
    while True:
        _print_table(target_name, params_map.keys(), data)
        char_name = input(f"请输入要删除的{target_name}名称：")
        if char_name in name_idx_map.keys():
            data.pop(name_idx_map[input])
            break
        else:
            print(f"无效的{target_name}名称，请重新输入")
            print()


def modify_stats(mode, data, chars=None):
    """
    This function will take action instructions from users and send data to the target functions
    The user interface follows the following logics:

        present the current data
        take input of the type of action
        take the action

    :param mode: the mode of the function, decided by the type of the data to be change
    :param data: the data to be change
    :param chars: the characters' info (only used for changing team)
    """
    buff_instruct = ""
    if mode == 'char':
        global _CHARS_PARAMS
        params = _CHARS_PARAMS
        a = '角色'
    elif mode == 'enemy':
        global _ENEMY_PARAMS
        params = _ENEMY_PARAMS
        a = '敌人'
    elif mode == 'team':
        global _TEAM_PARAMS
        params = _TEAM_PARAMS
        buff_instruct = "添加buff/"
        a = '队伍'
    else:
        raise

    while True:
        _print_table(a, params.keys(), data)

        print()
        instruction = input(f"请输入操作指令（修改/增加/删除/{buff_instruct}保存/quit）：")
        if instruction == "修改":
            _change_value(mode, data, chars)
        elif instruction == "增加":
            _add_new(mode, data, chars)
        elif instruction == "删除":
            _delete(mode, data, chars)
        elif instruction == "添加buff" and mode == "team":
            _buff_team(data)
        elif instruction == "保存":
            while True:
                direc = input("请输入保存地址:")
                try:
                    ExcelOperation.save_stats(data, direc)
                    break
                except:
                    print("无效地址，请重新输入")
                    print()
        elif instruction == "quit":
            print()
            break
        else:
            print("无效的操作指令，请重新输入")
            print()


def _buff_team(team):
    """
    This function will take instructions from users and buff skills
    The user interface follows the following logics:

        present the current data
        take input of the name of the value to be buffed
            take input of the idexes of the skills to be buffed
                take input of the value of the buff
                buff skills
            presenting the current data

    :param team: the team to be buffed
    """
    global _BUFF_PARAMS
    while True:
        _print_table('技能', _BUFF_PARAMS.keys(), team)
        buff_type = input("请选择添加buff的类别（技能倍率/百分比攻击/固定攻击/暴击率/暴击伤害/增伤/减抗/减防/独立乘区/quit）：")
        if buff_type in _BUFF_PARAMS.keys():
            while True:
                print("请输入被buff作用的技能的序号，示范：1-3,6,8,10-12（英文逗号）")
                buff_target = input("输入序号或quit：")
                if buff_target == 'quit':
                    break
                buff_targets = buff_target.split(',')
                target_skills_idx = []
                idx_work = True
                for target in buff_targets:
                    if re.match(r'^\d+$', target):
                        target_skills_idx.append(int(target)-1)
                    elif re.match(r'^\d+-\d+$', target):
                        _min, _max = re.match(r'^(\d+)-(\d+)$', target).groups()
                        target_skills_idx += list(range(int(_min)-1, int(_max)))
                    else:
                        idx_work = False
                        print("含有无效的技能序号，请重新输入")
                        print()
                        break

                while idx_work:
                    buff_value = input("请选择buff数值（数字/quit）：")
                    if buff_value == 'quit':
                        break
                    try:
                        buff_value = float(buff_value)
                        for skill in team[target_skills_idx]:
                            # print(skill)
                            _BUFF_PARAMS[buff_type](skill, buff_value)
                        break
                    except IndexError:
                        print("含有无效的技能序号，请重新输入")
                        print()
                    except ValueError:
                        print(f"无效的buff数值，请重新输入")
                        print()
                _print_table('技能', _BUFF_PARAMS.keys(), team)
        elif buff_type == 'quit':
            break
        else:
            print("")
            print()


def _create_team(name, chars):
    """
    This function will take instructions from users and create a tean
    The user interface follows the following logics:

    take input of the remarks of the team
        take input of the whether continue adding skill
            add skills by calling _add_new() function

    :param team: the team to be buffed
    """
    global _TEAM_PARAMS
    remark = input("请输入队伍备注")
    team = stats.Team(name, remark)

    while True:

        continue_add = input("是否继续添加技能（是/否）：")
        if continue_add == "是":
            _add_new('team', team, chars)
        elif continue_add == "否":
            break
        else:
            print(f"无效的回复，请重新输入")
            print()

        _print_table('技能', _BUFF_PARAMS.keys(), team)


def modify_teams(teams, chars):
    """
    UI logics for teams
    """
    name_idx_map = {team.name: idx for idx, team in enumerate(teams)}
    while True:
        team_name = input("请输入准备修改（新增）的队伍的名称（输入quit退出）：")
        if team_name in name_idx_map.keys():
            modify_stats('team', teams[name_idx_map[team_name]], chars)
        elif team_name == 'quit':
            break
        elif isinstance(team_name, str):
            while True:
                create_team = input("未寻到该队伍，是否新建队伍（是/否）：")
                if create_team == '是':
                    teams.append(_create_team(team_name, chars))
                    break
                elif create_team == '否':
                    break
                else:
                    print("未知指令，请重新输入")
                    print()
        else:
            print("无效的队伍名称，请重新输入队伍名称：")
            print()


def print_calculated_dmg(dmg_data, teams):
    """
    priting the damages of each team being against different enemies
    """
    print("输出结果")
    table = PrettyTable(['队伍'] + list(dmg_data.keys()))
    for team in teams:
        table.add_row([team.name] + [dmg_data[enemy][team.name] for enemy in dmg_data])
    print(table)


def calculate_dmg(enemies, teams, cal_method=stats.Team.calc_dmg):
    """
    calculate the damages of each team being against different enemies
    """
    dmg_data = {}
    for enemy in enemies:
        teams_dmg = {}
        for team in teams:
            teams_dmg.update(cal_method(team, enemy))
        dmg_data[enemy.name] = teams_dmg
    return dmg_data


def get_output(enemies, teams):
    """
    output the damages of each team being against different enemies
    """
    dmg_data = calculate_dmg(enemies, teams, cal_method=stats.Team.calc_chars_dmg)
    wb = Workbook()
    ws = wb.active
    ExcelOperation.output_worksheet(ws, dmg_data)
    while True:
        try:
            direc = input("请键入输出文件保存地址：")
            wb.save(direc)
            break
        except:
            print("无效地址，请重新输入")


if __name__ == '__main__':
    chars = ExcelOperation.char_dict(ExcelOperation.load_chars())
    enemies = ExcelOperation.load_enemies()
    teams = ExcelOperation.load_skills(chars, r".\data\v.1.1\c0c0.xlsx")
    for team in teams:
        name = team.name
        skills = team.skills
        # if "(低)" in name:
        #     skills_low = skills
        # elif "(高)" in name:
        #     print("\n队伍名称: ", name[:-3])
        #     enemy = enemies[0]
        #     l_dmg = 0
        #     h_dmg = 0
        #     for i in skills_low:
        #         l_dmg += i.calc_dmg(enemy)
        #     for i in skills:
        #         # i.print_info()
        #         h_dmg += i.calc_dmg(enemy)
        #
        #     print("队伍输出(" + enemy.name + "): ", l_dmg, " - ", h_dmg)
        # else:
        print("\n队伍名称: ", name)
        enemy = enemies[1]
        dmg = 0
        chars_dmg = defaultdict(lambda: 0)
        for i in skills:
            # i.print_info()
            dmg += i.calc_dmg(enemy)
            chars_dmg[i.char.name] += i.calc_dmg(enemy)
        print("队伍输出(" + enemy.name + "): ", dmg)
        for char_name in chars_dmg:
            print(f"{char_name}: {str(chars_dmg[char_name]/dmg*100)[0:6]}%")

