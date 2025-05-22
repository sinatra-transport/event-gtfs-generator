from generator import Generator
from grammar import event_time_definition, stop_sequence
from helpers import _on_color_light
from models import EventRoute, RouteInformation

if __name__ == "__main__":
    Generator(
        EventRoute(
            RouteInformation(
                "test",
                "Test Event",
                "Long Test Event",
                "131222",
                _on_color_light("131222")
            ),
            event_time_definition.parse("2025-05-10-2025-05-12//10:12-13:12/PT20M").value,
            stop_sequence.parse("asd122:PT1M,rffr2212,rffr22").value
        )
    ).generate("./output")
