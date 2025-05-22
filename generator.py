import datetime
from os import PathLike
from pathlib import Path
from typing import List, Dict

import pandas as pd
from isodate import Duration

from helpers import _sum_time, _time_output, _date_str_value, _div_time
from models import EventRoute, StopTravelTime


class Generator:
    model: EventRoute
    _trip_count: List[int]

    def __init__(self, model: EventRoute):
        self.model = model

    def generate(self, path: PathLike | str):
        self._trip_count = []
        self._generate_stop_times(path)
        self._generate_trips(path)
        self._generate_calendar(path)
        self._generate_calendar_dates(path)
        self._generate_routes(path)
        self._generate_stops(path)
        self._generate_shapes(path)

    def _generate_trips(self, path: PathLike | str):
        output = []

        for i, timing in enumerate(self.model.timing):
            for j in range(0, self._trip_count[i] - 1):
                output.append({
                    "route_id": self.model.info.route_id,
                    "service_id": timing.id(self.model.info.route_id),
                    "trip_id": f"{self.model.info.route_id}_{j}_{i}",
                    "trip_headsign": self.model.info.short_name,
                    "direction_id": "1",
                    "shape_id": f"{self.model.info.route_id}_shape",
                    "wheelchair_accessible": "0",
                    "bikes_allowed": "0"
                })

        df = pd.DataFrame(output)
        df.to_csv(Path(path).joinpath("trips.txt"), index=False)

    def _stop_time_model(
            self,
            timing_i: int,
            stop_i: int,
            counter: int,
            stop: StopTravelTime,
            current: Duration
    ) -> Dict:
        return {
            "trip_id": f"{self.model.info.route_id}_{timing_i}_{counter}",
            "arrival_time": _time_output(current),
            "departure_time": _time_output(current),
            "stop_id": stop.stop_id,
            "stop_sequence": f"{stop_i}",
            "stop_headsign": self.model.info.short_name,
            "pickup_type": "0",
            "drop_off_type": "0",
            "timepoint": "0"
        }

    def _generate_stop_times(self, path: PathLike | str):
        output = []
        comp = datetime.datetime.fromtimestamp(0)

        for i, timing in enumerate(self.model.timing):
            time = timing.timePeriod.start
            counter = 0
            while time.totimedelta(comp) <= timing.timePeriod.end.totimedelta(comp):
                increment = _div_time((
                        timing.repetitionDuration -
                        _sum_time([x.travel_time for x in self.model.stops if x.travel_time is not None])
                ), max(1, len(list(filter(lambda x: x.travel_time is None, self.model.stops)))))
                current = time
                for j, stop in enumerate(self.model.stops):
                    output.append(self._stop_time_model(
                        timing_i=i,
                        stop_i=j,
                        counter=counter,
                        stop=stop,
                        current=current,
                    ))
                    current += increment if stop.travel_time is None else stop.travel_time

                time += timing.repetitionDuration

                if self.model.is_loop:
                    output.append(self._stop_time_model(
                        timing_i=i,
                        stop_i=len(self.model.stops),
                        counter=counter,
                        stop=self.model.stops[0],
                        current=time,
                    ))

                counter += 1

            self._trip_count.append(counter)
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
        output = []
        for service in self.model.timing:
            output.append({
                "service_id": service.id(self.model.info.route_id),
            } | service.dayOfWeek.dict() | {
                "start_date": _date_str_value(service.datePeriod.start),
                "end_date": _date_str_value(service.datePeriod.end),
            })
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

    def _generate_shapes(self, path: PathLike | str):
        with Path(path).joinpath("shapes.txt").open("w") as f:
            f.write("shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence")