import datetime
from typing import List

from isodate import Duration


def _on_color_light(color: str) -> bool:
    # https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
    color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
    # https://stackoverflow.com/questions/3942878/how-to-decide-font-color-in-white-or-black-depending-on-background-color
    return (color[0] * 0.299 + color[1] * 0.587 + color[2] * 0.114) <= 186


def _sum_time(times: List[Duration]) -> Duration:
    out = Duration()
    for time in times:
        out += time

    return out


def _div_time(time: Duration, amount: int) -> Duration:
    return Duration(seconds=time.tdelta.total_seconds() // amount)


def _time_output(time: Duration) -> str:
    return ":".join([
        f"{time.tdelta.seconds // 3600}".zfill(2),
        f"{(time.tdelta.seconds // 60) % 60}".zfill(2),
    ])


def _dow_str_value(b: bool) -> str:
    return "1" if b else "0"


def _date_str_value(d: datetime.date) -> str:
    return "".join([
        f"{d.year}".zfill(4),
        f"{d.month}".zfill(2),
        f"{d.day}".zfill(2),
    ])
