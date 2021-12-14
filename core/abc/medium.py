from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from core.abc.station import AbstractStation
    from core.abc.frame import AbstractFrame


class AbstractMedium(ABC):
    propagation_speed: float
    stations: List["AbstractStation"]
    frames: List["AbstractFrame"]
    star_topology: bool
    center: Optional["AbstractStation"]

    @abstractmethod
    def set_center(self, station: "AbstractStation"):
        pass

    @abstractmethod
    def add_station(self, station: "AbstractStation"):
        pass

    @abstractmethod
    def add_frame(self, frame: "AbstractFrame"):
        pass

    @abstractmethod
    def remove_frame(self, frame: "AbstractFrame"):
        pass

    @abstractmethod
    def frame_count(self) -> int:
        pass

    @abstractmethod
    def get_random_receiver(self, sender: "AbstractStation") -> "AbstractStation":
        pass
