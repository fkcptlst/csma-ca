import os
import sys
from typing import Type, Dict
from multiprocessing import Pool

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
from utils.log import (
    log_result,
    logger_factory,
    station_notate,
    frame_notate,
    summary_settings,
)


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
        timeline.set_after_tick(logger_factory(settings))
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


def simulate_and_save_result(settings: Dict = default_settings):
    wire(settings)
    timeline = simulate()
    log_result(timeline, settings)


if __name__ == "__main__":
    debug = False
    overwrite = False

    try:
        if sys.argv[1] == "--debug":
            debug = True
        if sys.argv[1] == "--overwrite":
            overwrite = True
    except IndexError:
        pass

    if debug:
        wire(default_settings)
        timeline = simulate()
        exit()

    settings = (
        various_settings
        if overwrite
        else [
            settings
            for settings in various_settings
            if f"{summary_settings(settings)}.csv" not in os.listdir("results/csv")
        ]
    )

    pool = Pool(processes=16)
    pool.map(simulate_and_save_result, settings)
