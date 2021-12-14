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
        pass

    @abstractmethod
    def choose_receiver(self):
        pass

    @abstractmethod
    def okay_to_send(self, step: int) -> bool:
        pass
