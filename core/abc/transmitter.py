from abc import ABC, abstractmethod
from typing import List, Type, TypedDict, Union

from core.abc.csma import AbstractCSMA
from core.abc.frame import AbstractFrame, AbstractFrameStorage, FrameType


ProceedRecord = TypedDict(
    "ProceedRecord", {"typ": FrameType, "size": int, "count": int}
)


class AbstractTransmitter(ABC):
    station_id: int
    data_rate: int
    send_frames: AbstractFrameStorage
    recv_frames: AbstractFrameStorage
    detected_frames: AbstractFrameStorage

    recv: List[ProceedRecord]
    recv_current: int
    sent: List[ProceedRecord]
    sent_current: int
    collisions: int

    last_sent_data: Union[AbstractFrame, None]
    csma: AbstractCSMA
    with_rts: bool

    @abstractmethod
    def __init__(
        self,
        station_id: int,
        slot_time: int,
        data_rate: int,
        send_queue_size: int,
        recv_queue_size: int,
        with_rts: bool,
        frame_storage: Type[AbstractFrameStorage],
        csma: Type[AbstractCSMA],
    ):
        pass

    @abstractmethod
    def add_recv_record(self, frame: AbstractFrame):
        pass

    @abstractmethod
    def add_sent_record(self, frame: AbstractFrame):
        pass

    # receiver methods
    @abstractmethod
    def on_receive_success(self):
        pass

    @abstractmethod
    def on_receive_failure(self):
        pass

    @abstractmethod
    def on_timeout(self):
        pass

    @abstractmethod
    def on_detect(self, frame: AbstractFrame):
        pass

    @abstractmethod
    def talkover_detected(self) -> bool:
        pass

    @abstractmethod
    def is_medium_busy(self) -> bool:
        pass

    @abstractmethod
    def is_receiving(self) -> bool:
        pass

    @abstractmethod
    def proceed_recv(self, step: int):
        pass

    # sender methods
    @abstractmethod
    def push(self, frame: AbstractFrame):
        pass

    @abstractmethod
    def want_to_send(self) -> bool:
        pass

    @abstractmethod
    def is_sending(self) -> bool:
        pass

    @abstractmethod
    def proceed_send(self, step: int):
        pass

    @abstractmethod
    def send(self, step: int):
        pass

    # frame handlers
    @abstractmethod
    def on_data(self, frame: AbstractFrame):
        pass

    @abstractmethod
    def on_ack(self, frame: AbstractFrame):
        pass

    @abstractmethod
    def on_rts(self, frame: AbstractFrame):
        pass

    @abstractmethod
    def on_cts(self, frame: AbstractFrame):
        pass

    # access control
    @abstractmethod
    def okay_to_send(self, step: int) -> bool:
        pass
