import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from os import listdir, environ
from os.path import join
from argparse import ArgumentParser
import toml

TIMETABLES_DIRECTORY = environ.get("TIMETABLES_PY_TIMETABLES_DIRECTORY", "timetables")

timetables = [
    t.replace(".toml", "")
    for t in filter(lambda t: ".toml" in t, listdir(TIMETABLES_DIRECTORY))
]

parser = ArgumentParser(prog="timetable-py", description="Build timetable plots")
parser.add_argument(
    "timetable",
    type=str,
    choices=timetables,
    help="Select a timetable in the timetables directory",
)
parser.add_argument("via", type=str, action="append", help="Filter for via stops")
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
                    any([v.lower() in train_v.lower().split("/") for v in via])
                    for train_v in train["via"]
                ]
            ),
            trains,
        )
    )


def main():
    args = parser.parse_args()
    trains = filter_via(
        read_data(join(TIMETABLES_DIRECTORY, args.timetable + ".toml")), args.via
    )

    fig, ax = plt.subplots()
    plt.yticks(range(len(trains)), [train["name"] for train in trains])

    plt.eventplot(
        [train["departure"] for train in trains],
        colors=[train["color"] for train in trains] if all([train["color"] for train in trains]) else None,
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
