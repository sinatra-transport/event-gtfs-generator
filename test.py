from generator import Generator
from grammar import event_time_definition, stop_sequence
from helpers import _on_color_light
from models import EventRoute, RouteInformation

if __name__ == "__main__":
    Generator(
        EventRoute(
            RouteInformation(
                "floriade_2025_test",
                "Floriade",
                "Floriade 2025",
                "dc177a",
                _on_color_light("dc177a")
            ),
            event_time_definition.parse("2025-09-13-2025-10-12/1111100/09:00-17:15/PT40M").value,
            stop_sequence.parse("temp_floriade_mooseheads,3052,3356,temp_floriade_regatta").value
        )
    ).generate("./output")
