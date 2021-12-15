import random
from dependency_injector.wiring import Provide
from core.abc.csma import AbstractCSMA
from core.abc.frame import AbstractFrame
from core.container import DIContainer
from constant import (
    ONE_SECOND,
)
from utils.counter import Counter


class CSMA(AbstractCSMA):
    def __init__(
        self,
        data_rate: int,
        frame_size: int = Provide[DIContainer.settings.frame_size],
        slot_time: int = Provide[DIContainer.settings.slot_time],
        sifs_amount: int = Provide[DIContainer.settings.sifs],
        backoff_min: int = Provide[DIContainer.settings.backoff_min],
        backoff_max: int = Provide[DIContainer.settings.backoff_max],
    ):
        self.sifs_amount = sifs_amount
        self.difs_amount = sifs_amount + 2 * slot_time

        self.frame_time = int(frame_size / (data_rate / ONE_SECOND)) + 2 * slot_time
        self.rts_duration = 3 * sifs_amount + 3 * self.frame_time
        self.cts_duration = 2 * sifs_amount + 2 * self.frame_time
        self.backoff_min = backoff_min
        self.backoff_max = backoff_max
        self.backoff_range = backoff_min
        self.backoff = Counter(slot_time)
        self.nav = Counter()
        self.allocated = Counter()
        self.sifs = Counter()
        self.difs = Counter()

    def collision_occured(self):
        self.backoff_range = min(self.backoff_range * 2, self.backoff_max)

    def reset_backoff_range(self):
        self.backoff_range = self.backoff_min

    def set_backoff(self):
        self.backoff.reset(random.randint(0, self.backoff_range - 1))

    def set_sifs(self):
        self.sifs.reset(self.sifs_amount)

    def set_difs(self):
        self.difs.reset(self.difs_amount)

    def set_nav(self, duration: int):
        self.nav.reset(duration)

    def set_allocated(self, duration: int):
        self.allocated.reset(duration)

    def is_difs(self, with_rts: bool, frame: AbstractFrame):
        return (with_rts and frame.typ == "RTS") or (
            (not with_rts) and frame.typ == "DATA"
        )

    def nav_decrease(self, step: int):
        # decrease allocated time
        if self.allocated.is_left():
            self.allocated.decrease(step)

        # nav
        if self.nav.is_left():
            self.nav.decrease(step)

    def check_and_decrease(self, is_busy: bool, step: int):
        # should hibernate
        if self.nav.is_left():
            return False

        # wait for difs and sifs
        if self.sifs.is_left():
            self.sifs.decrease(step)
            return False

        if self.difs.is_left():
            self.difs.decrease(step)
            # difs just ended, set random backoff
            if not self.difs.is_left():
                self.set_backoff()
            return False

        # wait for backoff
        if self.backoff.is_left():
            if is_busy:
                self.set_difs()
                self.backoff.reset(0)
            else:
                self.backoff.decrease(step)
            return False

        # check the medium then set backoff
        if is_busy:
            self.set_difs()
            self.set_backoff()
            return False

        return True
