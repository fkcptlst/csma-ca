from typing import Type, Dict

from dependency_injector.wiring import Provide, inject
from constant import (
    MEGA,
    ONE_SECOND,
    SPEED_OF_LIGHT,
)
from core.implements import (
    Station,
    Transmitter,
    Medium,
    Frame,
    FrameRadius,
    FrameStorage,
    FramePath,
    FrameRadiusEdge,
    CSMA,
)
from core.time.line import TimeLine
from core.container import DIContainer
from utils.log import logger_factory, station_notate, frame_notate


@inject
def main(
    settings: Dict = Provide[DIContainer.config.settings],
    timeline: TimeLine = Provide[DIContainer.timeline],
    medium: Type[Medium] = Provide[DIContainer.medium],
):
    medium = medium(
        star_topology=settings["star_topology"],
        propagation_speed=settings["propagation_speed"],
        station_count=settings["station_count"],
        area_size=settings["area_size"],
    )
    medium.init_stations(
        data_rate=settings["data_rate"],
        frame_rate=settings["frame_rate"],
        detect_range=settings["detect_range"],
        slot_time=settings["slot_time"],
        with_rts=settings["with_rts"],
    )
    timeline.set_after_tick(logger_factory(medium, settings["with_rts"]))
    timeline.run()


if __name__ == "__main__":
    di_container = DIContainer()
    di_container.config.from_dict(
        {
            "settings": {
                "star_topology": True,
                "with_rts": True,
                "propagation_speed": SPEED_OF_LIGHT / 3,
                "area_size": 50,
                "station_count": 5,
                "data_rate": 11 * MEGA,
                "frame_rate": 100,
                "detect_range": 25,
                "frame_size": 1500,
                "backoff_min": 2,
                "backoff_max": 1024,
                "interval": 0.05,
                "slot_time": 20,
                "step": 20,
                "max_time": 1 * ONE_SECOND,
                "area_size": 50,
                "log_screen": True,
                "sifs": 10,
            },
            "notation": [
                {"instance": Station, "notation": station_notate},
                {"instance": Frame, "notation": frame_notate},
                {"instance": FramePath, "notation": "* "},
                {"instance": FrameRadiusEdge, "notation": "+ "},
                {"instance": FrameRadius, "notation": "- "},
                {"instance": "default", "notation": "  "},
            ],
            "medium": Medium,
            "station": Station,
            "frame": Frame,
            "frame_storage": FrameStorage,
            "transmitter": Transmitter,
            "csma": CSMA,
        }
    )
    di_container.wire(modules=[__name__])
    main()
