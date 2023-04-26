import toml
from sys import argv, exit
from os.path import exists

if len(argv) != 3:
    print("Help:")
    print("python scripts/old_color_to_new.py [timetable path] [color path]")
    exit(1)

timetable_path = argv[1]
color_path = argv[2]

if exists(color_path):
    if input(f"{color_path} already exists. Overwrite? (y/n)") != "y":
        exit(0)

colors = {
    train["name"]: train["color"] for train in toml.load(timetable_path)["trains"]
}
with open(color_path, "w") as file:
    file.write(toml.dumps(colors))
