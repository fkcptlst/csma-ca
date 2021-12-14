from typing import Type

from dependency_injector.wiring import Provide, inject
from constant import (
    AREA_SIZE,
    STATION_COUNT,
    STATION_DETECT_RANGE,
    STEP,
    USE_RTS_CTS,
    STAR_TOPOLOGY,
)
from core.implements import (
    Station,
    Medium,
    Frame,
    FrameRadius,
    Transmitter,
    FrameStorage,
    CSMA,
)
from core.timeline import TimeLine, TimeLineContainer
from utils.helper import get_random_location
from utils.log import logger_factory, station_notate, frame_notate


@inject
def main(timeline: TimeLine = Provide[TimeLineContainer.timeline]):
    rts_cts = USE_RTS_CTS
    star_topology = STAR_TOPOLOGY

    station_type: Type[Station] = Station
    if rts_cts:
        station_type = Station

    medium = Medium(star_topology=star_topology)
    medium.register()

    for i in range(0, STATION_COUNT):
        center = star_topology and i == 0

        location = get_random_location(AREA_SIZE)
        if star_topology and not center:
            location = get_random_location(AREA_SIZE, STATION_DETECT_RANGE - 1)
        elif star_topology and center:
            location = (AREA_SIZE // 2, AREA_SIZE // 2)

        station = station_type(
            id=i,
            location=location,
            medium=medium,
            transmitter=Transmitter,
            frame=Frame,
            frame_storage=FrameStorage,
            csma=CSMA,
            with_rts=rts_cts,
        )
        station.register()

        if center:
            medium.set_center(station)

    timeline.set_after_tick(logger_factory(medium, rts_cts))
    timeline.run()


if __name__ == "__main__":
    time_line_container = TimeLineContainer()
    time_line_container.config.from_dict(
        {
            "notation": [
                {"instance": Station, "notation": station_notate},
                {"instance": Frame, "notation": frame_notate},
                {"instance": FrameRadius, "notation": "- "},
                {"instance": "default", "notation": "  "},
            ],
            "log_screen": True,
            "step": STEP,
        }
    )
    time_line_container.wire(modules=[__name__])
    main()
