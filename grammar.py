import datetime

import isodate
from petitparser import character as c

from models import DayOfWeek, DatePeriod, TimePeriod, ServiceTiming, StopTravelTime

i_separator = c.of('/')

year = (c.digit().times(4) | c.digit().times(2)).flatten().map(lambda x: int(x))
month = c.digit().times(2).flatten().map(lambda x: int(x))
day = c.digit().times(2).flatten().map(lambda x: int(x))
d_separator = c.of('-')

date = (year & d_separator & month & d_separator & day).map(lambda x: datetime.date(
    x[0],
    month=x[2],
    day=x[4]
))
date_period = ((date & d_separator & date) | date).map(lambda x: DatePeriod.from_array(x))

hour_part = c.digit().repeat(1, 2).flatten().map(lambda x: int(x))
time_part = c.digit().times(2).flatten().map(lambda x: int(x))
t_separator = c.of(':')

time = ((hour_part & t_separator & time_part & (t_separator & time_part).optional())
        .map(lambda x: datetime.time(
            hour=x[0],
            minute=x[2],
            second=x[4] if len(x) > 4 else 0
        )))
time_period = ((time & d_separator & time) | time).map(lambda x: TimePeriod.from_array(x))

day_of_week = ((c.of('1') | c.of('0')).times(7).optional()
               .map(lambda x: DayOfWeek.from_array(x)))

duration = ((c.of("P") &
             (c.digit().repeat(1, 4) & c.of("Y")).optional() &
             (c.digit().repeat(1, 2) & c.of("M")).optional() &
             (c.digit().repeat(1, 2) & c.of("D")).optional() &
             (c.of("T") &
              (c.digit().repeat(1, 2) & c.of("H")).optional() &
              (c.digit().repeat(1, 2) & c.of("M")).optional() &
              (c.digit().repeat(1, 2) & c.of("S")).optional()).optional())
).flatten().map(lambda x: isodate.parse_duration(x))

event_time_definition = (
        date_period & i_separator &
        day_of_week & i_separator &
        time_period & i_separator &
        duration
).map(lambda x: ServiceTiming(
    x[0],
    x[4],
    x[2],
    x[6]
))

stop_id = (c.digit() | c.letter()).plus().flatten()
stop_travel_time = (stop_id & (c.of(":") & duration).optional()).map(lambda x: StopTravelTime.from_array(x))
stop_sequence = (stop_travel_time.separated_by(c.of(","))).plus().map(lambda x: x[0][0::2])

print(event_time_definition.parse("2025-05-10-2025-05-12//10:12-13:12/PT20M").value)
print(stop_sequence.parse("asd122:PT12H,rffr2212,rffr2212"))
