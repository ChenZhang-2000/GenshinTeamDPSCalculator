import yaml

_config_direc = r".\configs"

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

with open(rf"{_config_direc}\stats_position_map.yaml", 'r', encoding="utf-8") as stream:
    stats_pos_map = yaml.safe_load(stream)

char_map = {alias: obj for obj in _char_map for alias in _char_map[obj]}
weapon_map = {alias: obj for obj in _weapon_map for alias in _weapon_map[obj]}
artifact_map = {alias: obj for obj in _artifact_map for alias in _artifact_map[obj]}
enemy_map = {alias: obj for obj in _enemy_map for alias in _enemy_map[obj]}
enemy_header_map = {alias: obj for obj in _enemy_header_map for alias in _enemy_header_map[obj]}
stats_map = {alias: obj for obj in _stats_map for alias in _stats_map[obj]}
