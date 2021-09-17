from common import ui, exl_operation as ExcelOperation


def main():
    char_dir = r".\data\characters.xlsx"  # input("请输入角色信息表格文件地址：")
    enemy_dir = r".\data\enemy.xlsx"  # input("请输入敌人信息表格文件地址：")
    team_dir = r".\data\skills.xlsx"  # input("请输入队伍技能循环表格文件地址：")

    chars = ExcelOperation.load_chars(char_dir)
    enemies = ExcelOperation.load_enemies(enemy_dir)
    teams = ExcelOperation.load_skills({char.name: char for char in chars}, team_dir)

    # print(chars)
    ui.main_loop(chars, enemies, teams)

    return


if __name__ == "__main__":
    main()
