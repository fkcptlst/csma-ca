import random
from typing import Tuple, Type

from core.abc.frame import AbstractFrame, AbstractFrameStorage

from core.abc.station import AbstractStation
from core.abc.transmitter import AbstractTransmitter
from core.abc.csma import AbstractCSMA
from core.timeline import TimeParticipant
from constant import (
    ONE_SECOND,
    STATION_DATA_RATE,
    STATION_DETECT_RANGE,
    STATION_FRAME_RATE,
    SLOT_TIME,
    ACK_TIMEOUT,
)

from .medium import Medium


class Station(AbstractStation, TimeParticipant):
    send_queue_size: int = 10
    recv_queue_size: int = 1
    detect_range: float = STATION_DETECT_RANGE
    slot_time: int = SLOT_TIME
    frame: Type[AbstractFrame]
    data_rate: int = STATION_DATA_RATE
    frame_rate: float = STATION_FRAME_RATE
    sent: int = 0
    timeout: int = ACK_TIMEOUT
    with_rts: bool = True

    def __init__(
        self,
        id: int,
        location: Tuple[float, float],
        with_rts: bool,
        medium: Medium,
        transmitter: Type[AbstractTransmitter],
        frame: Type[AbstractFrame],
        frame_storage: Type[AbstractFrameStorage],
        csma: Type[AbstractCSMA],
    ):
        self.id = id
        self.location = location
        self.with_rts = with_rts
        self.medium = medium
        self.frame = frame
        self.transmitter = transmitter(
            station_id=self.id,
            slot_time=self.slot_time,
            data_rate=self.data_rate,
            send_queue_size=self.send_queue_size,
            recv_queue_size=self.recv_queue_size,
            with_rts=self.with_rts,
            frame_storage=frame_storage,
            csma=csma,
        )
        self.medium.add_station(self)

    def want_to_push(self) -> bool:
        if self.transmitter.send_frames.get():
            return False

        if self.transmitter.csma.allocated.is_left():
            return False

        return random.random() < (self.timeline.step * self.frame_rate / ONE_SECOND)

    def choose_receiver(self):
        return self.medium.get_random_receiver(self)

    def check_okay_to_send(self) -> bool:
        # access control check
        if not self.transmitter.okay_to_send(self.timeline.step):
            return False

        # not in the same slot
        if self.timeline.current % self.slot_time != 0:
            return False

        return True

    def on_tick_init(self, step: int):
        self.transmitter.detected = None

    def on_tick(self, step):
        if self.transmitter.last_sent is not None:
            if self.transmitter.last_sent.sent + self.timeout < self.timeline.current:
                self.transmitter.last_sent = None
                self.transmitter.on_timeout()

        if self.transmitter.is_sending():
            self.transmitter.proceed_send(step)
            return

        if self.transmitter.is_receiving():
            self.transmitter.proceed_recv(step)
            return

        if self.want_to_push():
            receiver = self.choose_receiver()
            if receiver is not None:
                self.transmitter.push(
                    self.frame.assemble(
                        receiver=receiver,
                        sender=self,
                        typ="RTS",
                        duration=self.transmitter.csma.rts_duration,
                    )
                    if self.with_rts
                    else self.frame.assemble(
                        receiver=receiver,
                        sender=self,
                        typ="DATA",
                    )
                )

        if self.check_okay_to_send():
            if not self.transmitter.send_frames.is_empty():
                self.transmitter.send(step)
