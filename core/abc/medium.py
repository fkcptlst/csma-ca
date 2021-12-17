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
        """Add initial stations to the medium.

        Parameters
        ----------
        data_rate : float
            The data rate of the station.
        frame_rate : float
            The frame rate of the station.
        detect_range : float
            The detect range of the station.
        slot_time : int
            The slot time of the station.
        timeout : int
            Amount of the timeout of the station.
        with_rts : bool
            Whether the station can send RTS frame.
        station_type : Type[AbstractStation]
            The type of the station.
        """
        pass

    @abstractmethod
    def set_center(self, station: "AbstractStation"):
        """Set the station as the center of the medium.

        If star_topology is enabled, the stations will send every frames to the central station

        Parameters
        ----------
        station : AbstractStation
            The station to be set as the center.
        """
        pass

    @abstractmethod
    def add_station(self, station: "AbstractStation"):
        """Add a station to the medium.

        Parameters
        ----------
        station : AbstractStation
            The station to be added.
        """
        pass

    @abstractmethod
    def add_frame(self, frame: "AbstractFrame"):
        """Add a frame to the medium.

        Added frame would be considered as on air.

        Parameters
        ----------
        frame : AbstractFrame
            The frame to be added.
        """
        pass

    @abstractmethod
    def remove_frame(self, frame: "AbstractFrame"):
        """Remove the frame from the medium.

        Removed frame would be considered as off air.

        Parameters
        ----------
        frame : AbstractFrame
            The frame to be removed.
        """
        pass

    @abstractmethod
    def frame_count(self) -> int:
        """Get the number of frames in the medium.

        Returns
        -------
        int
            The number of frames in the medium.
        """
        pass

    @abstractmethod
    def get_random_receiver(self, sender: "AbstractStation") -> "AbstractStation":
        """Get a random receiver station from the medium.

        The receiver station would be different from the sender station and be in the range of the sender station.

        Parameters
        ----------
        sender : AbstractStation
            The sender station.

        Returns
        -------
        AbstractStation
            The random receiver station.
        """
        pass
