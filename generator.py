import datetime
from os import PathLike
from pathlib import Path

import pandas as pd

from helpers import _sum_time, _time_output, _date_str_value
from models import EventRoute


class Generator:
    model: EventRoute
    _trip_count: int

    def __init__(self, model: EventRoute):
        self.model = model

    def generate(self, path: PathLike | str):
        self._generate_stop_times(path)
        self._generate_trips(path)
        self._generate_calendar(path)
        self._generate_calendar_dates(path)
        self._generate_routes(path)
        self._generate_stops(path)

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

    def _generate_routes(self, path: PathLike | str):
        output = [{
            "route_id": self.model.info.route_id,
            "route_short_name": self.model.info.short_name,
            "route_long_name": self.model.info.long_name,
            "route_type": "3",
            "route_color": self.model.info.color,
            "route_text_color": "FFFFFF" if self.model.info.light_text_color else "000000",
            "route_url": "https://www.transport.act.gov.au/getting-around/timetables/routes-by-number",
            "agency_id": "TC"
        }]
        df = pd.DataFrame(output)
        df.to_csv(Path(path).joinpath("routes.txt"), index=False)

    def _generate_calendar(self, path: PathLike | str):
        output = [{
            "service_id": f"{self.model.info.route_id}_service",
        } | self.model.timing.dayOfWeek.dict() | {
            "start_date": _date_str_value(self.model.timing.datePeriod.start),
            "end_date": _date_str_value(self.model.timing.datePeriod.end),
        }]
        df = pd.DataFrame(output)
        df.to_csv(Path(path).joinpath("calendar.txt"), index=False)

    def _generate_calendar_dates(self, path: PathLike | str):
        with Path(path).joinpath("calendar_dates.txt").open("w") as f:
            f.write("service_id,date,exception_type")

    def _generate_stops(self, path: PathLike | str):
        output = []
        for stop in self.model.stops:
            output.append({
                "stop_id": stop.stop_id,
                "stop_name": "",
                "stop_lat": "",
                "stop_lon": "",
                "location_type": "0",
                "wheelchair_boarding": "0",
                "parent_station": ""
            })

        df = pd.DataFrame(output)
        df.to_csv(Path(path).joinpath("stops.txt"), index=False)