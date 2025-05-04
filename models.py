from dataclasses import dataclass


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
            DayOfWeek(
                x[0] == "1",
                x[1] == "1",
                x[2] == "1",
                x[3] == "1",
                x[4] == "1",
                x[5] == "1",
                x[6] == "1",
            )
        else:
            DayOfWeek(
                True,
                True,
                True,
                True,
                True,
                True,
                True,
            )
