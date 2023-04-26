import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from os import environ
from os.path import join, exists
from argparse import ArgumentParser
from resources.iris import get_station_eva, get_timetable
import toml

TIMETABLES_DIRECTORY = environ.get("TIMETABLES_PY_TIMETABLES_DIRECTORY", "timetables")
COLORS_DIRECTORY = environ.get(
    "TIMETABLES_PY_COLORS_DIRECTORY", join(TIMETABLES_DIRECTORY, "colors")
)

parser = ArgumentParser(prog="timetable-py", description="Build timetable plots")
parser.add_argument(
    "-i",
    "--iris",
    type=str,
    help="Hour range of iris fetch if you want ot use iris. Example: 10-12",
)
parser.add_argument(
    "timetable",
    type=str,
    help="Select a timetable in the timetables directory or a station name if you want to use iris",
)
parser.add_argument("via", type=str, action="append", help="Filter for via stops")
parser.add_argument(
    "-s",
    "--station",
    type=str,
    help="Overwrite the timetable for iris by another station name (e.g. use 'FF' instead of 'frankfurt' because 'frankfurt' is FFT)",
)
parser.add_argument(
    "-o",
    "--output",
    type=str,
    help="Save the plot as an image to a file instead of showing it",
)


# read the timetables data from a file
def read_data(file):
    trains = toml.load(file)["trains"]
    for train in trains:
        if "departure" in train:
            train["departure"] = [
                datetime.strptime(departure, "%H:%M")
                for departure in train["departure"]
            ]
    return trains


# filter a trains list for via stops
def filter_via(trains, via: list[str]):
    return list(
        filter(
            lambda train: any(
                [
                    any(
                        [
                            any(
                                [
                                    (v.lower() in k.split(" ") or v.lower() == k)
                                    for k in train_v.lower().split("/")
                                ]
                            )
                            for v in via
                        ]
                    )
                    for train_v in train["via"]
                ]
            ),
            trains,
        )
    )


def main():
    args = parser.parse_args()
    trains = []
    if args.iris:
        f, t = args.iris.split("-")
        hours = range(int(f), int(t))
        departures = []
        eva = get_station_eva(args.station if args.station else args.timetable)
        for hour in hours:
            departures.extend(get_timetable(eva, datetime.now().date(), hour))
        trains_ungrouped = [
            {
                "name": train["category"] + " " + train["departure"]["line"],
                "departure": [train["departure"]["time"]],
                "via": train["departure"]["stops"],
                "line": train["departure"]["line"],
            }
            for train in filter(
                lambda train: "departure" in train and "line" in train["departure"],
                departures,
            )
        ]
        trains = {}
        for train in trains_ungrouped:
            key = train["name"] + str(train["via"][0])
            if key in trains:
                trains[key]["departure"].extend(train["departure"])
            else:
                trains[key] = train
        trains = trains.values()
    else:
        trains = read_data(join(TIMETABLES_DIRECTORY, args.timetable + ".toml"))

    trains = filter_via(trains, args.via)
    trains = sorted(trains, key=lambda train: train["name"].split(" ")[0])
    trains = sorted(
        trains,
        key=lambda train: train["line"]
        if "line" in train
        else int(train["name"].split(" ")[1]),
        reverse=True,
    )

    colors_path = join(COLORS_DIRECTORY, args.timetable.lower() + ".toml")
    if exists(colors_path):
        colors = toml.load(colors_path)
        for train in trains:
            for color_name, color in colors.items():
                if "color" not in train and (
                    train["name"].replace(" ", "") in color_name.replace(" ", "")
                    or color_name.replace(" ", "") in train["name"].replace(" ", "")
                ):
                    train["color"] = color
                    break
    not_colored = list(filter(lambda train: "color" not in train, trains))
    if not_colored:
        print(
            "These trains doesn't have a color: ",
            ", ".join([train["name"] for train in not_colored]),
        )

    fig, ax = plt.subplots()
    plt.yticks(range(len(trains)), [train["name"] for train in trains])

    plt.eventplot(
        [train["departure"] for train in trains],
        colors=[train["color"] if "color" in train else "b" for train in trains],
        linelengths=0.2,
        linewidths=10,
    )
    plt.gcf().autofmt_xdate()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.set_xlabel("Departure")
    ax.set_title(
        f"Trains in {args.timetable} in the direction of {', '.join(args.via)}"
    )

    if args.output:
        plt.savefig(args.output)
    else:
        plt.show()
