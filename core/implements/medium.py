import random
from typing import List, Type

from dependency_injector.wiring import Provide
from core.abc.medium import AbstractMedium
from core.abc.station import AbstractStation
from core.abc.frame import AbstractFrame
from core.container import DIContainer

from core.timeline import TimeParticipant
from utils.helper import get_distance, get_random_location, is_location_equal


class Medium(AbstractMedium, TimeParticipant):
    def __init__(
        self,
        star_topology: bool,
        propagation_speed: float,
        station_count: int,
        area_size: int,
    ):
        self.propagation_speed = propagation_speed
        self.stations: List[AbstractStation] = []
        self.frames: List[AbstractFrame] = []
        self.star_topology = star_topology
        self.area_size = area_size
        self.station_count = station_count
        self.center = None
        self.register()

    def init_stations(
        self,
        data_rate: float,
        frame_rate: float,
        detect_range: float,
        slot_time: int,
        timeout: int,
        with_rts: bool,
        station_type: Type[AbstractStation] = Provide[DIContainer.station],
    ):
        for i in range(0, self.station_count):
            center = self.star_topology and i == 0

            location = get_random_location(self.area_size)
            if self.star_topology and not center:
                location = get_random_location(self.area_size, detect_range - 1)
            elif self.star_topology and center:
                location = (self.area_size // 2, self.area_size // 2)

            station = station_type(
                id=i,
                location=location,
                medium=self,
                data_rate=data_rate,
                frame_rate=frame_rate,
                detect_range=detect_range,
                slot_time=slot_time,
                timeout=timeout,
                with_rts=with_rts,
            )

            if center:
                self.set_center(station)

    def set_center(self, station: AbstractStation):
        self.center = station

    def add_station(self, station: AbstractStation):
        self.stations.append(station)

    def add_frame(self, frame: AbstractFrame):
        self.frames.append(frame)

    def remove_frame(self, frame: AbstractFrame):
        self.frames.remove(frame)

    def frame_count(self) -> int:
        return len(set([f.id for f in self.frames]))

    def get_random_receiver(self, sender: AbstractStation) -> AbstractStation:
        if self.star_topology:
            if sender.id == self.center.id:
                return None
            return self.center

        stations = [
            station
            for station in self.stations
            if sender.id != station.id
            and get_distance(station.location, sender.location) < sender.detect_range
        ]
        if len(stations) == 0:
            return None
        return random.choice(stations)

    def on_tick_init(self, step: int):
        for station in self.stations:
            station.transmitter.detected_frames.clear()

        for frame in self.frames:
            if not frame.sent:
                return

            for station in self.stations:
                if station.id == frame.sender.id:
                    continue

                for radius in frame.radius:
                    if is_location_equal(radius.location, station.location):
                        station.transmitter.on_detect(frame)
                        break

            if frame.moved_tail >= frame.max_range and not frame.vanished:
                frame.vanish()

        self.frames = [f for f in self.frames if not f.vanished]
