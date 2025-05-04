import isodate
from petitparser import character as c

from models import DayOfWeek

i_separator = c.of('/')

year = (c.digit().times(4) | c.digit().times(2))
month = c.digit().times(2)
day = c.digit().times(2)
d_separator = c.of('-')

date = (year & d_separator & month & d_separator & day)
date_period = (date & d_separator & date) | date

time_part = c.digit().times(2)
t_separator = c.of(':')

time = (time_part & t_separator & time_part & (t_separator & time_part).optional())
time_period = (time & d_separator & time) | time

day_of_week = ((c.of('1') | c.of('0')).times(7).optional()
               )

duration = ((c.of("P") &
            (c.digit().repeat(1, 4) & c.of("Y")).optional() &
            (c.digit().repeat(1, 2) & c.of("M")).optional() &
            (c.digit().repeat(1, 2) & c.of("D")).optional() &
            (c.of("T") &
             (c.digit().repeat(1, 2) & c.of("H")).optional() &
             (c.digit().repeat(1, 2) & c.of("M")).optional() &
             (c.digit().repeat(1, 2) & c.of("S")).optional()).optional())
            ).flatten().map(lambda x: isodate.parse_duration(x))

event_time_definition = (date_period & i_separator & day_of_week.optional() & i_separator & time_period & i_separator & duration)

print(event_time_definition.parse("2025-05-10-2025-05-12/1011111/10:12-12:12/PT20M").value)
