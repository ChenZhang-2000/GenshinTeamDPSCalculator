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
    package_dir={"GTDC": "GTDC"},
    package_data={"GTDC": ["*.yaml", "*.json"]},
    install_requires=['torch', 'numpy', 'pandas', 'matplotlib', 'PyYAML'],
)

# ['GTDC',
#  'GTDC.common', 'GTDC.common.artifact', 'GTDC.common.characters', 'GTDC.common.enemy', 'GTDC.common.weapon',
#  'GTDC.common.artifact', 'GTDC.common.characters.stats', 'GTDC.common.enemy.stats', 'GTDC.common.weapon.stats',
#  'GTDC.configs', 'GTDC.tools'],
