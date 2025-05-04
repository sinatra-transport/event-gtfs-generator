import datetime
from dataclasses import dataclass
from time import strftime
from typing import Optional

from isodate import Duration


@dataclass
class DayOfWeek:
    monday: bool
    tuesday: bool
    wednesday: bool
    thursday: bool
    friday: bool
    saturday: bool
    sunday: bool

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
    start: datetime.time
    end: Optional[datetime.time]

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
            self.datePeriod.start.strftime('%Y-%m-%d'),
            self.datePeriod.end.strftime('%Y-%m-%d') if self.datePeriod.end else None,
            route_id
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
