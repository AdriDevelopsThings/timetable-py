from setuptools import setup

setup(
    name="timetable-py",
    version="0.1.0",
    description="Generate timetable plots",
    author="AdriDoesThings",
    author_email="contact@adridoesthings.com",
    packages=["resources"],
    entry_points={"console_scripts": ["timetable-py=resources:main"]},
    install_requires=["toml", "matplotlib", "argparse"],
)
