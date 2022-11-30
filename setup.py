from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='GTDC',
    version='0.1.0',
    author='Chen Zhang',
    author_email='academic@chenzhang.me',
    description='Testing installation of Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ChenZhang-2000/GenshinTeamDPSCalculator',
    project_urls={
        "Bug Tracker": "https://github.com/ChenZhang-2000/GenshinTeamDPSCalculator/issues"
    },
    license='GPL',
    packages=find_packages(where="."),
    include_package_data=True,
    package_dir={"GTDC": "GTDC",
                 "config": "GTDC/configs",
                 "kw_map": "GTDC/configs/kw_map",
                 "artifact_stats": "GTDC/common/artifact/stats",
                 "char_stats": "GTDC/common/characters/stats",
                 "enemy_stats": "GTDC/common/enemy/stats",
                 "weapon_stats": "GTDC/common/weapon/stats",},
    package_data={"GTDC": ["*.yaml", "*.json"]},
    data_files=[("GTDC/configs", ["GTDC/configs/*.yaml", "GTDC/configs/*.json"]),
                ("GTDC/configs/kw_map", ["GTDC/configs/kw_map/*.yaml", "GTDC/configs/kw_map/*.json"]),
                ("GTDC/common/artifact/stats", ["GTDC/common/artifact/stats/*.yaml", "GTDC/common/artifact/stats/*.json"]),
                ("GTDC/common/characters/stats", ["GTDC/common/characters/stats/*.yaml", "GTDC/common/characters/stats/*.json"]),
                ("GTDC/common/enemy/stats", ["GTDC/common/enemy/stats/*.yaml", "GTDC/common/enemy/stats/*.json"]),
                ("GTDC/common/weapon/stats", ["GTDC/common/weapon/stats/*.yaml", "GTDC/common/weapon/stats/*.json"]),
                ],
    install_requires=['torch', 'numpy', 'pandas', 'matplotlib', 'PyYAML'],
)

# ['GTDC',
#  'GTDC.common', 'GTDC.common.artifact', 'GTDC.common.characters', 'GTDC.common.enemy', 'GTDC.common.weapon',
#  'GTDC.common.artifact', 'GTDC.common.characters.stats', 'GTDC.common.enemy.stats', 'GTDC.common.weapon.stats',
#  'GTDC.configs', 'GTDC.tools'],
