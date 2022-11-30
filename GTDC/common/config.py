import os

import yaml


_config_direc = os.path.join(os.path.dirname(__file__), rf'..\configs')

with open(rf"{_config_direc}\kw_map\char_map.yaml", 'r', encoding="utf-8") as stream:
    _char_map = yaml.safe_load(stream)
with open(rf"{_config_direc}\kw_map\weapon_map.yaml", 'r', encoding="utf-8") as stream:
    _weapon_map = yaml.safe_load(stream)
with open(rf"{_config_direc}\kw_map\artifact_map.yaml", 'r', encoding="utf-8") as stream:
    _artifact_map = yaml.safe_load(stream)
with open(rf"{_config_direc}\kw_map\enemy_map.yaml", 'r', encoding="utf-8") as stream:
    _enemy_map = yaml.safe_load(stream)
with open(rf"{_config_direc}\kw_map\stats_map.yaml", 'r', encoding="utf-8") as stream:
    _stats_map = yaml.safe_load(stream)

with open(rf"{_config_direc}\kw_map\enemy_header_map.yaml", 'r', encoding="utf-8") as stream:
    _enemy_header_map = yaml.safe_load(stream)
with open(rf"{_config_direc}\kw_map\skill_header_map.yaml", 'r', encoding="utf-8") as stream:
    _skill_header_map = yaml.safe_load(stream)
with open(rf"{_config_direc}\kw_map\skill_map.yaml", 'r', encoding="utf-8") as stream:
    _skill_map = yaml.safe_load(stream)
with open(rf"{_config_direc}\kw_map\reaction_map.yaml", 'r', encoding="utf-8") as stream:
    _reaction_map = yaml.safe_load(stream)

with open(rf"{_config_direc}\stats_position_map.yaml", 'r', encoding="utf-8") as stream:
    stats_pos_map = yaml.safe_load(stream)

char_map = {alias: obj for obj in _char_map for alias in _char_map[obj]}
weapon_map = {alias: obj for obj in _weapon_map for alias in _weapon_map[obj]}
artifact_map = {alias: obj for obj in _artifact_map for alias in _artifact_map[obj]}
enemy_map = {alias: obj for obj in _enemy_map for alias in _enemy_map[obj]}
enemy_header_map = {alias: obj for obj in _enemy_header_map for alias in _enemy_header_map[obj]}
skill_header_map = {alias: obj for obj in _skill_header_map for alias in _skill_header_map[obj]}
skill_map = {alias: obj for obj in _skill_map for alias in _skill_map[obj]}
stats_map = {alias: obj for obj in _stats_map for alias in _stats_map[obj]}

reaction_map = {alias: obj for obj in _reaction_map for alias in _reaction_map[obj]}
reaction_map[''] = None
