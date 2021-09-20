from common import ui, exl_operation as ExcelOperation
import openpyxl.utils.exceptions


def main():
    while True:
        char_dir = input("请输入角色信息表格文件地址：")  # r".\data\characters.xlsx"  #
        try:
            chars = ExcelOperation.load_chars(char_dir)
            break
        except openpyxl.utils.exceptions.InvalidFileException:
            print("无效的文件地址")
        except Exception as e:
            print(e.__class__)
            print(e.args)

    while True:
        enemy_dir = input("请输入敌人信息表格文件地址：")  # r".\data\enemy.xlsx"  #
        try:
            enemies = ExcelOperation.load_enemies(enemy_dir)
            break
        except openpyxl.utils.exceptions.InvalidFileException:
            print("无效的文件地址")
        except Exception as e:
            print(e.__class__)
            print(e.args)

    while True:
        team_dir = input("请输入队伍技能循环表格文件地址：")  # r".\data\skills.xlsx"  #
        try:
            teams = ExcelOperation.load_skills({char.name: char for char in chars}, team_dir)
            break
        except openpyxl.utils.exceptions.InvalidFileException:
            print("无效的文件地址")
        except Exception as e:
            print(e.__class__)
            print(e.args)

    # print(chars)
    ui.main_loop(chars, enemies, teams)

    return


if __name__ == "__main__":
    main()
