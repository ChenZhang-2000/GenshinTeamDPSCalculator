import yaml
import openpyxl
import torch

from common.stats import STATS_LENGTH
from common.model import Model, Team
from common.characters import CHAR_FACTORY
from common.weapon import WEAPON_FACTORY
from common.artifact import ArtifactSet, ARTIFACT_FACTORY
from common.enemy import ENEMY_FACTORY
from common import config


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
                                                       constellation=data['char']['constellation'],
                                                       name=data['name'])
        chars.append(character)
    team = Team(*chars)
    return team


def read_char_excel(file_direc=r".\data\characters.xlsx"):
    ws = openpyxl.load_workbook(file_direc, data_only=True).worksheets[0]
    chars = []
    header = [config.stats_map[cell.value] for cell in ws[1]]
    data_map = config.stats_pos_map
    for row in ws.iter_rows(min_row=2):
        artifact_data = torch.zeros(STATS_LENGTH)
        char_data = {}
        for i, cell in enumerate(row):
            value = cell.value
            if i <= 7:
                char_data[header[i]] = value
            else:
                value = 0. if value is None else float(value)
                artifact_data[data_map[header[i]]] = value
        char_data = {'name': char_data['name'],
                     'char': {'name': config.char_map[char_data['character']],
                              'level': int(char_data['character_level']),
                              'constellation': int(char_data['character_constellation'])},
                     'weapon': {'name': config.weapon_map[char_data['weapon']],
                                'affix': int(char_data['weapon_affix'])},
                     'artifact': {'two_set': config.artifact_map[char_data['artifact_two']],
                                  'four_set': config.artifact_map[char_data['artifact_four']],
                                  'stats': artifact_data.reshape(1,STATS_LENGTH)}}
        chars.append(char_data)
    return chars


def read_enemy_excel(file_direc=r".\data\enemy.xlsx"):
    ws = openpyxl.load_workbook(file_direc, data_only=True).worksheets[0]
    enemies = {}
    header = [config.enemy_header_map[cell.value] for cell in ws[1]]
    for row in ws.iter_rows(min_row=2):
        enemy_data = {}
        for i, cell in enumerate(row):
            value = cell.value
            enemy_data[header[i]] = value
        enemies[enemy_data['name']] = ENEMY_FACTORY[config.enemy_map[enemy_data['enemy']]](enemy_data['enemy_level'])
    return enemies
    # print(chars)
