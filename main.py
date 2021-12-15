from typing import Type

from dependency_injector.wiring import Provide, inject
from constant import (
    ACK_TIMEOUT,
    AREA_SIZE,
    PROPAGATION_SPEED,
    SLOT_TIME,
    STAR_TOPOLOGY,
    STATION_COUNT,
    STATION_DATA_RATE,
    STATION_FRAME_RATE,
    STEP,
    USE_RTS_CTS,
    STATION_DETECT_RANGE,
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
from core.timeline import TimeLine
from core.container import DIContainer
from utils.log import logger_factory, station_notate, frame_notate


@inject
def main(
    timeline: TimeLine = Provide[DIContainer.timeline],
    medium: Type[Medium] = Provide[DIContainer.medium],
):
    medium = medium(
        star_topology=STAR_TOPOLOGY,
        propagation_speed=PROPAGATION_SPEED,
        station_count=STATION_COUNT,
        area_size=AREA_SIZE,
    )
    medium.init_stations(
        data_rate=STATION_DATA_RATE,
        frame_rate=STATION_FRAME_RATE,
        detect_range=STATION_DETECT_RANGE,
        slot_time=SLOT_TIME,
        timeout=ACK_TIMEOUT,
        with_rts=USE_RTS_CTS,
    )
    timeline.set_after_tick(logger_factory(medium, USE_RTS_CTS))
    timeline.run()


if __name__ == "__main__":
    di_container = DIContainer()
    di_container.config.from_dict(
        {
            "timeline": {
                "notation": [
                    {"instance": Station, "notation": station_notate},
                    {"instance": Frame, "notation": frame_notate},
                    {"instance": FramePath, "notation": "* "},
                    {"instance": FrameRadiusEdge, "notation": "+ "},
                    {"instance": FrameRadius, "notation": "- "},
                    {"instance": "default", "notation": "  "},
                ],
                "log_screen": True,
                "step": STEP,
            },
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
