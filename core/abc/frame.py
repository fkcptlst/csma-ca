from abc import ABC, abstractmethod
from typing import Optional, Union, Literal
from typing import TYPE_CHECKING, List, Tuple

if TYPE_CHECKING:
    from .station import AbstractStation


FrameType = Union[Literal["DATA"], Literal["ACK"], Literal["RTS"], Literal["CTS"]]


class AbstractFrame(ABC):
    id: str
    typ: FrameType
    sender: "AbstractStation"
    receiver: "AbstractStation"
    duration: Optional[int]

    max_range: int
    size: int

    sent: Optional[int]
    sent_done: Optional[int]
    vanished: Optional[int]

    # department and arrival
    @abstractmethod
    def depart(self):
        """Depart, start sending

        Register the frame to the timeline and set the sent time.
        The frame with sent time and with out vanished time is considered as on air.
        """
        pass

    @abstractmethod
    def done(self):
        """Done sending

        Set the sent_done time.
        sent_done - sent would be the transmission delay.
        """
        pass

    @abstractmethod
    def vanish(self):
        """Vanish if the frame is out of the range"""
        pass

    # locations
    @property
    @abstractmethod
    def moved(self) -> float:
        """Get the moved distance

        Returns
        -------
        float
            The moved distance
        """
        pass

    @property
    @abstractmethod
    def moved_tail(self) -> float:
        """Get the moved distance of the tail of the frame

        Returns
        -------
        float
            The moved distance of the tail of the frame
        """
        pass

    @property
    @abstractmethod
    def location(self) -> Tuple[float, float]:
        """Get the location of the frame

        Returns
        -------
        Tuple[float, float]
            The location of the frame
        """
        pass

    @property
    def location_tail(self) -> Tuple[float, float]:
        """Get the location of the tail of the frame

        Returns
        -------
        Tuple[float, float]
            The location of the tail of the frame
        """
        pass

    @property
    @abstractmethod
    def distance(self) -> float:
        """Get the distance between the sender and the receiver

        Returns
        -------
        float
            The distance between the sender and the receiver
        """
        pass

    # frame properties
    @staticmethod
    @abstractmethod
    def assemble(
        receiver: "AbstractStation",
        sender: "AbstractStation",
        typ: FrameType = "DATA",
        duration: Optional[int] = None,
    ) -> "AbstractFrame":
        """Assemble a new frame

        Parameters
        ----------
        receiver : AbstractStation
            The receiver of the frame
        sender : AbstractStation
            The sender of the frame
        typ : FrameType, optional
            The type of the frame, by default "DATA"
        duration : Optional[int], optional
            The duration of the frame, by default None

        Returns
        -------
        AbstractFrame
            The assembled frame
        """
        pass

    @abstractmethod
    def is_equal(self, frame: "AbstractFrame") -> bool:
        """Check if the frame is equal to the given frame

        Parameters
        ----------
        frame : AbstractFrame
            The frame to compare with

        Returns
        -------
        bool
            True if the frame is equal to the given frame
        """
        pass

    @abstractmethod
    def icon(self) -> str:
        """Get the icon of the frame

        Returns
        -------
        str
            The icon of the frame
        """
        pass


class AbstractFrameStorage(ABC):
    """Queue of frames"""

    frames: List[AbstractFrame] = []
    size: int

    @abstractmethod
    def is_empty(self) -> bool:
        """Check if the frame storage is empty

        Returns
        -------
        bool
            True if the frame storage is empty
        """
        pass

    @abstractmethod
    def is_full(self) -> bool:
        """Check if the frame storage is full

        Returns
        -------
        bool
            True if the frame storage is full
        """
        pass

    @abstractmethod
    def count(self) -> int:
        """Get the count of the frame storage

        Returns
        -------
        int
            The count of the frame storage
        """
        pass

    @abstractmethod
    def all(self) -> List[AbstractFrame]:
        """Get all the frames in the frame storage

        Returns
        -------
        List[AbstractFrame]
            All the frames in the frame storage
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear the frame storage"""
        pass

    @abstractmethod
    def get(self) -> Optional[AbstractFrame]:
        """Get a frame from the frame storage

        Returns
        -------
        Optional[AbstractFrame]
            The frame from the frame storage
        """
        pass

    @abstractmethod
    def push(self, frame) -> None:
        """Push a frame into the frame storage

        Parameters
        ----------
        frame : AbstractFrame
            The frame to push into the frame storage
        """
        pass

    @abstractmethod
    def pop(self) -> Optional[AbstractFrame]:
        """Pop a frame from the frame storage

        Returns
        -------
        Optional[AbstractFrame]
            The popped frame from the frame storage
        """
        pass
