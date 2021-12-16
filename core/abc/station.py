from abc import ABC, abstractmethod
from typing import Optional, Tuple, Type
from core.abc.frame import AbstractFrame
from core.abc.medium import AbstractMedium
from core.abc.transmitter import AbstractTransmitter


class AbstractStation(ABC):
    id: int
    location: Tuple[int, int]
    medium: AbstractMedium
    transmitter: AbstractTransmitter
    send_queue_size: Optional[int]
    recv_queue_size: Optional[int]
    detect_range: float
    slot_time: int
    data_rate: int
    frame: Type[AbstractFrame]
    frame_rate: float
    last_sent: AbstractFrame
    sent: int
    timeout: int
    with_rts: bool

    @abstractmethod
    def want_to_push(self) -> bool:
        """Check if the station have any frame to send.

        Sending frame storage of it's transmitter must be empty,
        allocated counter must be expired.

        Then calculate the probability of new frame with it's frame rate.
        """
        pass

    @abstractmethod
    def choose_receiver(self) -> "AbstractStation":
        """Choose the random receiver in the detect range of the station."""
        pass

    @abstractmethod
    def okay_to_send(self, step: int) -> bool:
        """Check if the station can send a frame.

        The result of ``transmitter.okay_to_send`` must be true,
        sending frame storage of it's transmitter must be empty,
        and the current time must be at the slot time.
        """
        pass
