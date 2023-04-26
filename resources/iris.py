import requests
import xmltodict
from datetime import date, datetime


def get_station_eva(name: str) -> str:
    text = requests.get(
        "https://iris.noncd.db.de/iris-tts/timetable/station/" + name
    ).text
    return xmltodict.parse(text)["stations"]["station"]["@eva"]


def get_train_from_xml(train):
    d = {"category": train["tl"]["@c"]}

    if "ar" in train:
        d["arrival"] = {
            "stops": train["ar"]["@ppth"].split("|"),
            "time": datetime.strptime(train["ar"]["@pt"], "%y%m%d%H%M"),
        }
        if "@l" in train["ar"]:
            d["arrival"]["line"] = train["ar"]["@l"]
    if "dp" in train:
        d["departure"] = {
            "stops": train["dp"]["@ppth"].split("|"),
            "time": datetime.strptime(train["dp"]["@pt"], "%y%m%d%H%M"),
        }
        if "@l" in train["dp"]:
            d["departure"]["line"] = train["dp"]["@l"]
    return d


def get_timetable(eva: str, date: date, hour: int):
    text = requests.get(
        f"https://iris.noncd.db.de/iris-tts/timetable/plan/{eva}/{date.strftime('%y%m%d')}/{hour:02}"
    ).text
    if not text:
        return []
    xml = xmltodict.parse(text)
    if "timetable" not in xml or not xml["timetable"]:
        return []
    if type(xml["timetable"]["s"]) == dict:
        xml["timetable"]["s"] = [xml["timetable"]["s"]]
    return [get_train_from_xml(train) for train in xml["timetable"]["s"]]
