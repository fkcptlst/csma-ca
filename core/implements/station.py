import random
from typing import Tuple, Type

from dependency_injector.wiring import Provide, inject

from core.abc.frame import AbstractFrame, AbstractFrameStorage
from core.abc.station import AbstractStation
from core.abc.transmitter import AbstractTransmitter
from core.abc.csma import AbstractCSMA
from core.abc.medium import AbstractMedium
from core.time.participant import TimeParticipant
from core.container import DIContainer
from constant import (
    ONE_SECOND,
)


class Station(AbstractStation, TimeParticipant):
    send_queue_size: int = 10
    recv_queue_size: int = 1
    frame: Type[AbstractFrame]
    sent: int = 0
    with_rts: bool = True

    @inject
    def __init__(
        self,
        id: int,
        location: Tuple[float, float],
        medium: AbstractMedium,
        data_rate: int,
        frame_rate: int,
        detect_range: float,
        slot_time: int,
        with_rts: bool,
        transmitter: Type[AbstractTransmitter] = Provide[DIContainer.transmitter],
        frame: Type[AbstractFrame] = Provide[DIContainer.frame],
        frame_storage: Type[AbstractFrameStorage] = Provide[DIContainer.frame_storage],
        csma: Type[AbstractCSMA] = Provide[DIContainer.csma],
    ):
        self.id = id
        self.location = location
        self.medium = medium
        self.with_rts = with_rts
        self.data_rate = data_rate
        self.frame_rate = frame_rate
        self.detect_range = detect_range
        self.slot_time = slot_time

        self.frame = frame
        self.transmitter = transmitter(
            station_id=self.id,
            data_rate=self.data_rate,
            send_queue_size=self.send_queue_size,
            recv_queue_size=self.recv_queue_size,
            with_rts=self.with_rts,
            frame_storage=frame_storage,
            csma=csma,
        )
        self.register()
        self.medium.add_station(self)

    def want_to_push(self) -> bool:
        if self.transmitter.send_frames.get():
            return False

        if self.transmitter.csma.allocated.is_left():
            return False

        return random.random() < (self.timeline.step * self.frame_rate / ONE_SECOND)

    def choose_receiver(self):
        return self.medium.get_random_receiver(self)

    def okay_to_send(self, step: int) -> bool:
        return (
            self.transmitter.okay_to_send(step)
            and (not self.transmitter.send_frames.is_empty())
            and (self.timeline.current % self.slot_time == 0)
        )

    def on_tick(self, step):
        if self.transmitter.timeout_occured(self.timeline.current):
            self.transmitter.on_timeout()

        self.transmitter.csma.nav_decrease(step)

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

        if self.okay_to_send(step):
            self.transmitter.send(step)
