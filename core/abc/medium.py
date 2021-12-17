from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Optional, Type

if TYPE_CHECKING:
    from core.abc.station import AbstractStation
    from core.abc.frame import AbstractFrame


class AbstractMedium(ABC):
    propagation_speed: float
    stations: List["AbstractStation"]
    frames: List["AbstractFrame"]
    star_topology: bool
    center: Optional["AbstractStation"]
    station_count: int
    area_size: int

    @abstractmethod
    def init_stations(
        self,
        data_rate: float,
        frame_rate: float,
        detect_range: float,
        slot_time: int,
        timeout: int,
        with_rts: bool,
        station_type: Type["AbstractStation"],
    ):
        """ """
        pass

    @abstractmethod
    def set_center(self, station: "AbstractStation"):
        """ """
        pass

    @abstractmethod
    def add_station(self, station: "AbstractStation"):
        """ """
        pass

    @abstractmethod
    def add_frame(self, frame: "AbstractFrame"):
        """ """
        pass

    @abstractmethod
    def remove_frame(self, frame: "AbstractFrame"):
        """ """
        pass

    @abstractmethod
    def frame_count(self) -> int:
        """ """
        pass

    @abstractmethod
    def get_random_receiver(self, sender: "AbstractStation") -> "AbstractStation":
        """ """
        pass
