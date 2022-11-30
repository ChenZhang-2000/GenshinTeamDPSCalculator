import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
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
    packages=['GTDC', 'common', 'configs', 'tools'],
    install_requires=['torch', 'numpy', 'pandas', 'matplotlib', 'PyYAML'],
)