import datetime
from os import PathLike
from pathlib import Path
from typing import List

import pandas as pd
from isodate import Duration

from models import EventRoute


def _sum_time(times: List[Duration]) -> Duration:
    out = Duration()
    for time in times:
        out += time

    return out


def _time_output(time: Duration) -> str:
    return ":".join([
        f"{time.tdelta.seconds // 3600}".zfill(2),
        f"{(time.tdelta.seconds // 60) % 60}".zfill(2),
    ])


class Generator:
    model: EventRoute
    _trip_count: int

    def __init__(self, model: EventRoute):
        self.model = model

    def generate(self, path: PathLike | str):
        self._generate_stop_times(path)
        self._generate_trips(path)
        pass

    def _generate_trips(self, path: PathLike | str):
        output = []

        for i in range(0, self._trip_count - 1):
            output.append({
                "route_id": self.model.info.route_id,
                "service_id": f"{self.model.info.route_id}_service",
                "trip_id": f"{self.model.info.route_id}_{i}",
                "trip_headsign": self.model.info.short_name,
                "direction_id": "1",
                "shape_id": f"{self.model.info.route_id}_shape",
                "wheelchair_accessible": "0",
                "bikes_allowed": "0"
            })

        df = pd.DataFrame(output)
        df.to_csv(Path(path).joinpath("trips.txt"), index=False)
        # day = self.model.timing.datePeriod.start
        # while day < self.model.timing.datePeriod.end:
        #     if not self.model.timing.dayOfWeek.allowed(day.weekday()):
        #         day += datetime.timedelta(days=1)
        #         continue
        #
        #
        #
        #     day += datetime.timedelta(days=1)
        # pass

    def _generate_stop_times(self, path: PathLike | str):
        output = []
        comp = datetime.datetime.fromtimestamp(0)

        time = self.model.timing.timePeriod.start
        counter = 0
        while time.totimedelta(comp) <= self.model.timing.timePeriod.end.totimedelta(comp):
            increment = (
                    self.model.timing.repetitionDuration -
                    _sum_time([x.travel_time for x in self.model.stops if x.travel_time is not None])
            )
            current = time
            for i, stop in enumerate(self.model.stops):
                output.append({
                    "trip_id": f"{self.model.info.route_id}_{counter}",
                    "arrival_time": _time_output(current),
                    "departure_time": _time_output(current),
                    "stop_id": stop.stop_id,
                    "stop_sequence": f"{i}",
                    "stop_headsign": self.model.info.short_name,
                    "pickup_type": "0",
                    "drop_off_type": "0",
                    "timepoint": "0"
                })
                current += increment if stop.travel_time is None else stop.travel_time

            counter += 1
            time += self.model.timing.repetitionDuration

        self._trip_count = counter
        df = pd.DataFrame(output)
        df.to_csv(Path(path).joinpath("stop_times.txt"), index=False)

