from generator import Generator
from grammar import event_time_definition, stop_sequence
from helpers import _on_color_light
from models import EventRoute, RouteInformation

if __name__ == "__main__":
    Generator(
        EventRoute(
            RouteInformation(
                "floriade_2025_test",
                "F1",
                "TEST Floriade 2025 Free Shuttle Loop",
                "dc177a",
                _on_color_light("dc177a")
            ),
            [
                event_time_definition.parse("2025-09-13-2025-10-12/1111100/09:00-17:55/PT40M").value,
                event_time_definition.parse("2025-09-13-2025-10-12/0000011/09:00-17:35/PT20M").value,
                event_time_definition.parse("2025-09-29-2025-10-02/1111111/18:00-23:05/PT20M").value
            ],
            stop_sequence.parse("temp_floriade_mooseheads:PT5M,3052:PT5M,3356:PT5M,temp_floriade_regatta:PT5M").value
        )
    ).generate("./output")
