# Timetable-py
Generate timetable plots like this:


![Example timetable from erfurt via weimar](screenshots/timetable_erfurt.png)

## Installation
A python version >= 3.8 is required. Install timetable-py with ``python setup.py install`` and run ``timetable-py`` or run the main.py with ``python main.py`` directly.

## Arguments
```
usage: timetable-py [-h] [-i IRIS] [-s STATION] [-m] [-o OUTPUT] timetable via

Build timetable plots

positional arguments:
  timetable             Select a timetable in the timetables directory or a station name if you want to use iris
  via                   Filter for via stops

options:
  -h, --help            show this help message and exit
  -i IRIS, --iris IRIS  Hour range of iris fetch if you want ot use iris. Example: 10-12
  -s STATION, --station STATION
                        Overwrite the timetable for iris by another station name (e.g. use 'FF' instead of 'frankfurt' because 'frankfurt' is FFT)
  -m, --merge           Merge all trains in one line
  -o OUTPUT, --output OUTPUT
                        Save the plot as an image to a file instead of showing it
```

## Write timetable files
A timetable file is a [TOML](https://toml.io/en/) file with a `trains` list. Every `trains` item should be look like like this:
```
[[trains]]
name = "RB 20"
via = ["Weimar, "Naumburg", "Leipzig"] # it will be possible to filter for via stops
departure = ["00:01", "01:01"] # this means the train departures at minute 1 every hour. (if you try to show trains with a maximum 2 hour cycle that means you show 2 hours in your plot)
color = "#24589B"
``` 