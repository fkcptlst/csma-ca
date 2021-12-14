import random
from typing import List, TYPE_CHECKING
from core.abc.medium import AbstractMedium
from core.abc.station import AbstractStation
from core.abc.frame import AbstractFrame

from core.timeline import TimeParticipant
from utils.helper import get_distance, is_location_equal
from constant import (
    PROPAGATION_SPEED,
)


class Medium(AbstractMedium, TimeParticipant):
    def __init__(
        self, star_topology: bool = False, propagation_speed: float = PROPAGATION_SPEED
    ):
        self.propagation_speed = propagation_speed
        self.stations: List[AbstractStation] = []
        self.frames: List[AbstractFrame] = []
        self.star_topology = star_topology
        self.center = None

    def set_center(self, station: AbstractStation):
        self.center = station

    def add_station(self, station: AbstractStation):
        self.stations.append(station)

    def add_frame(self, frame: AbstractFrame):
        self.frames.append(frame)

    def remove_frame(self, frame: AbstractFrame):
        self.frames.remove(frame)

    def frame_count(self) -> int:
        return len([f for f in self.frames if not f.is_duplicate])

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

    def on_tick(self, step: int):
        for frame in self.frames:
            if not frame.sent:
                return

            for station in self.stations:
                if station.id == frame.sender.id:
                    continue

                for radius in frame.radius:
                    if is_location_equal(radius.location, station.location):
                        frame.arrive(station)

            if frame.moved >= frame.max_range:
                frame.vanish()
                self.frames.remove(frame)
