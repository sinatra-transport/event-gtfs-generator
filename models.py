import datetime
from dataclasses import dataclass
from typing import Optional, List

from isodate import Duration

from helpers import _dow_str_value


@dataclass
class DayOfWeek:
    monday: bool
    tuesday: bool
    wednesday: bool
    thursday: bool
    friday: bool
    saturday: bool
    sunday: bool

    def allowed(self, weekday: int) -> bool:
        if weekday == 0 and self.monday:
            return True
        elif weekday == 1 and self.tuesday:
            return True
        elif weekday == 2 and self.wednesday:
            return True
        elif weekday == 3 and self.thursday:
            return True
        elif weekday == 4 and self.friday:
            return True
        elif weekday == 5 and self.saturday:
            return True
        elif weekday == 6 and self.saturday:
            return True
        return False

    def dict(self) -> dict[str, str]:
        return {
            "monday": _dow_str_value(self.monday),
            "tuesday": _dow_str_value(self.tuesday),
            "wednesday": _dow_str_value(self.wednesday),
            "thursday": _dow_str_value(self.thursday),
            "friday": _dow_str_value(self.friday),
            "saturday": _dow_str_value(self.saturday),
            "sunday": _dow_str_value(self.sunday),
        }

    def id(self) -> str:
        return "".join([
            _dow_str_value(self.monday),
            _dow_str_value(self.tuesday),
            _dow_str_value(self.wednesday),
            _dow_str_value(self.thursday),
            _dow_str_value(self.friday),
            _dow_str_value(self.saturday),
            _dow_str_value(self.sunday),
        ])

    @staticmethod
    def from_array(x) -> "DayOfWeek":
        if x:
            return DayOfWeek(
                x[0] == "1",
                x[1] == "1",
                x[2] == "1",
                x[3] == "1",
                x[4] == "1",
                x[5] == "1",
                x[6] == "1",
            )
        else:
            return DayOfWeek(
                True,
                True,
                True,
                True,
                True,
                True,
                True,
            )


@dataclass
class DatePeriod:
    start: datetime.date
    end: Optional[datetime.date]

    @staticmethod
    def from_array(x) -> "DatePeriod":
        if len(x) == 1:
            return DatePeriod(x[0], None)
        else:
            return DatePeriod(x[0], x[2])


@dataclass
class TimePeriod:
    start: Duration
    end: Optional[Duration]

    @staticmethod
    def from_array(x) -> "TimePeriod":
        if len(x) == 1:
            return TimePeriod(x[0], None)
        else:
            return TimePeriod(x[0], x[2])


@dataclass
class ServiceTiming:
    datePeriod: DatePeriod
    timePeriod: TimePeriod
    dayOfWeek: DayOfWeek
    repetitionDuration: Duration

    def id(self, route_id: str) -> str:
        elements = [
            route_id,
            self.datePeriod.start.strftime('%Y%m%d'),
            self.datePeriod.end.strftime('%Y%m%d') if self.datePeriod.end else None,
            self.dayOfWeek.id()
        ]
        return '-'.join(list(filter(lambda x: x is not None, elements)))


@dataclass
class StopTravelTime:
    stop_id: str
    travel_time: Optional[Duration]

    @staticmethod
    def from_array(x) -> "StopTravelTime":
        if x[1] is None:
            return StopTravelTime(x[0], None)
        else:
            return StopTravelTime(x[0], x[1][1])


@dataclass
class RouteInformation:
    route_id: Optional[str]
    short_name: str
    long_name: str
    color: str
    light_text_color: bool


@dataclass
class EventRoute:
    info: RouteInformation
    timing: List[ServiceTiming]
    stops: List[StopTravelTime]

