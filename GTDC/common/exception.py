from .characters import CHAR_FACTORY
from .weapon import WEAPON_FACTORY
from .artifact import ARTIFACT_FACTORY
from .enemy import ENEMY_FACTORY
from .config import char_map, weapon_map, artifact_map, enemy_map


class InvalidModel(Exception):
    pass


class InvalidSkillTime(InvalidModel):
    pass


class InvalidCell(Exception):
    def __init__(self, cell, ws_idx=0):
        self.value = cell.value
        self.col_idx = cell.column_letter
        self.row_idx = cell.row
        self.ws_idx = ws_idx


class InvalidTitle(InvalidCell):
    def __init__(self, cell, ws_idx=0):
        super().__init__(cell, ws_idx)


class InvalidValue(InvalidCell):
    def __init__(self, cell, ws_idx=0):
        super().__init__(cell, ws_idx)


class InvalidCharacterName(InvalidValue):
    def __init__(self, cell, ws_idx=0):
        super().__init__(cell, ws_idx)


class InvalidCharacterLevel(InvalidValue):
    def __init__(self, cell, ws_idx=0):
        super().__init__(cell, ws_idx)


class InvalidStats(InvalidValue):
    def __init__(self, cell, ws_idx=0):
        super().__init__(cell, ws_idx)


class InvalidWeaponName(InvalidValue):
    def __init__(self, cell, ws_idx=0):
        super().__init__(cell, ws_idx)


class InvalidArtifactName(InvalidValue):
    def __init__(self, cell, ws_idx=0):
        super().__init__(cell, ws_idx)


class InvalidConstellation(InvalidValue):
    def __init__(self, cell, ws_idx=0):
        super().__init__(cell, ws_idx)


class InvalidAffix(InvalidValue):
    def __init__(self, cell, ws_idx=0):
        super().__init__(cell, ws_idx)


class InvalidSkillLevel(InvalidValue):
    def __init__(self, cell, ws_idx=0):
        super().__init__(cell, ws_idx)


class EmptyCell(InvalidValue):
    def __init__(self, cell, ws_idx=0):
        super().__init__(cell, ws_idx)


def invalid_cell_value(cell_exception: InvalidCell):
    return f"无法识别表格{cell_exception.ws_idx+1}中单元格{cell_exception.col_idx}{cell_exception.row_idx}的值：{cell_exception.value}"


def invalid_char_file(err):
    """
    :param err: InvalidCell
    :return:
    """
    if isinstance(err, InvalidTitle):
        err_type = "表头"
    elif isinstance(err, InvalidCharacterName):
        err_type = "角色名称"
    elif isinstance(err, InvalidCharacterLevel):
        err_type = "角色等级"
    elif isinstance(err, InvalidConstellation):
        err_type = "角色命座"
    elif isinstance(err, InvalidSkillLevel):
        err_type = "角色技能等级"
    elif isinstance(err, InvalidWeaponName):
        err_type = "武器名称"
    elif isinstance(err, InvalidAffix):
        err_type = "武器精炼"
    elif isinstance(err, InvalidArtifactName):
        err_type = "圣遗物名称"
    elif isinstance(err, InvalidStats):
        err_type = "属性"
    elif isinstance(err, EmptyCell):
        err_type = "基础属性有空，识别"
    else:
        raise err
    print(f"角色信息表格{err_type}错误：")
    print(f"  {invalid_cell_value(err)}")


def varify_char_file(value_type, cell, ws=0):
    if type(cell.value) not in [str, int, float]:
        raise EmptyCell(cell, ws)
    if value_type == "name":
        pass
    elif value_type == "character":
        if cell.value not in char_map:
            raise InvalidCharacterName(cell, ws)
    elif value_type == "character_level":
        value = cell.value
        if value[-1] == '+':
            value = value[:-1]
        try:
            int_value = int(value)
            if int_value < 0:
                raise InvalidCharacterLevel(cell, ws)
        except ValueError:
            raise InvalidCharacterLevel(cell, ws)
    elif value_type == "character_constellation":
        value = cell.value
        try:
            int_value = int(value)
            if int_value < 0 or int_value > 6:
                raise InvalidConstellation(cell, ws)
        except ValueError:
            raise InvalidConstellation(cell, ws)
    elif value_type == "skill_level":
        levels = cell.value.split(',')
        for value in levels:
            try:
                int_value = int(value)
                if int_value < 0 or int_value > 10:
                    raise InvalidSkillLevel(cell, ws)
            except ValueError:
                raise InvalidSkillLevel(cell, ws)
    elif value_type == "weapon":
        if cell.value not in weapon_map:
            raise InvalidWeaponName(cell, ws)
    elif value_type == "weapon_affix":
        value = cell.value
        try:
            int_value = int(value)
            if int_value < 0 or int_value > 5:
                raise InvalidAffix(cell, ws)
        except ValueError:
            raise InvalidAffix(cell, ws)
    elif value_type == "artifact_two":
        if cell.value not in artifact_map:
            raise InvalidArtifactName(cell, ws)
    elif value_type == "artifact_four":
        if cell.value not in artifact_map:
            raise InvalidArtifactName(cell, ws)
    else:
        raise ValueError("Invalid value_type" + value_type)


class InvalidEnemyName(InvalidCell):
    def __init__(self, cell, ws_idx=0):
        super().__init__(cell, ws_idx)


class InvalidEnemyLevel(InvalidCell):
    def __init__(self, cell, ws_idx=0):
        super().__init__(cell, ws_idx)


def invalid_enemy_file(err):
    if isinstance(err, InvalidEnemyName):
        err_type = "角色名称"
    elif isinstance(err, InvalidEnemyLevel):
        err_type = "角色等级"
    elif isinstance(err, EmptyCell):
        err_type = "基础属性有空，识别"
    else:
        raise err
    print(f"敌人信息表格{err_type}错误：")
    print(f"  {invalid_cell_value(err)}")


def varify_enemy_file(value_type, cell, ws=0):
    if type(cell.value) not in [str, int, float]:
        # print(type(cell.value))
        raise EmptyCell(cell, ws)
    if value_type == "name":
        pass
    elif value_type == "enemy":
        if cell.value not in enemy_map:
            raise InvalidEnemyName(cell, ws)
    elif value_type == "enemy_level":
        value = cell.value
        try:
            int_value = int(value)
            if int_value < 0:
                raise InvalidEnemyLevel(cell, ws)
        except ValueError:
            raise InvalidEnemyLevel(cell, ws)


class InvalidSkillName(InvalidCell):
    def __init__(self, cell, ws_idx=0):
        super().__init__(cell, ws_idx)


class InvalidBuffName(InvalidCell):
    def __init__(self, cell, ws_idx=0):
        super().__init__(cell, ws_idx)


class InvalidIndex(InvalidCell):
    def __init__(self, cell, ws_idx=0):
        super().__init__(cell, ws_idx)


class InvalidCharNameInSkillFile(InvalidIndex):
    def __init__(self, cell, ws_idx=0):
        super().__init__(cell, ws_idx)


class MissingIndex(InvalidIndex):
    def __init__(self, ws_idx):
        self.ws_idx = ws_idx


class MissingTime(MissingIndex):
    def __init__(self, ws_idx=0):
        super().__init__(ws_idx)


class MissingSkills(MissingIndex):
    def __init__(self, ws_idx=0):
        super().__init__(ws_idx)


class MissingBuffs(MissingIndex):
    def __init__(self, ws_idx=0):
        super().__init__(ws_idx)


class MissingOnField(MissingIndex):
    def __init__(self, ws_idx=0):
        super().__init__(ws_idx)


def invalid_skill_file(err):
    pass


def invalid_skill_index(err):
    if isinstance(err, MissingIndex):
        if isinstance(err, MissingTime):
            print(f"表格{err.ws_idx}缺少时间轴注明")
        elif isinstance(err, MissingSkills):
            print(f"表格{err.ws_idx}缺少技能循环注明")
        elif isinstance(err, MissingBuffs):
            print(f"表格{err.ws_idx}缺少增益效果注明")
        elif isinstance(err, MissingOnField):
            print(f"表格{err.ws_idx}缺少战场角色注明")

    elif isinstance(err, InvalidCharNameInSkillFile):
        print(f"表格{err.ws_idx}的{err.col_idx}{err.row_idx}单元格有一个无法识别的角色名：{err.value}")


def varify_skill_file(value_type, cell, ws=0):
    pass
