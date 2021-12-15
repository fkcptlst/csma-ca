from typing import Type, Dict

from dependency_injector.wiring import Provide, inject

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
from config import default_settings
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
    timeline.set_after_tick(logger_factory(medium, settings["frame_size"]))
    timeline.run()


if __name__ == "__main__":
    di_container = DIContainer()
    di_container.config.from_dict(
        {
            "settings": {
                **default_settings,
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
