from abc import ABC, abstractmethod
from typing import Type, Union

from core.abc.csma import AbstractCSMA
from core.abc.frame import AbstractFrame, AbstractFrameStorage


class AbstractTransmitter(ABC):
    station_id: int
    frame_rate: int
    send_frames: AbstractFrameStorage
    recv_frames: AbstractFrameStorage

    received: int
    received_current: int
    received_data: int
    sent: int
    sent_current: int
    collisions: int

    last_sent_data: Union[AbstractFrame, None]
    detected: AbstractFrame
    csma: AbstractCSMA
    with_rts: bool

    @abstractmethod
    def __init__(
        self,
        station_id: int,
        slot_time: int,
        frame_rate: int,
        send_queue_size: int,
        recv_queue_size: int,
        with_rts: bool,
        frame_storage: Type[AbstractFrameStorage],
        csma: Type[AbstractCSMA],
    ):
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
