import sys
from typing import Type, Dict

from tqdm import tqdm
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
from config import default_settings, various_settings
from utils.log import log_result, logger_factory, station_notate, frame_notate


@inject
def simulate(
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
    if settings["log"]:
        timeline.set_after_tick(logger_factory(medium, settings["frame_size"]))
    timeline.run()
    return timeline


def wire(settings: Dict = default_settings):
    di_container = DIContainer()
    di_container.config.from_dict(
        {
            "settings": {
                **settings,
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


def main():
    for settings in tqdm(various_settings):
        wire(settings)
        timeline = simulate()
        log_result(timeline, settings)


if __name__ == "__main__":
    if sys.argv[1] == "--debug":
        wire(default_settings)
        timeline = simulate()
    else:
        main()
