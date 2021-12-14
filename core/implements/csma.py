import random
from core.abc.csma import AbstractCSMA
from core.abc.frame import AbstractFrame
from constant import (
    CTS_DURATION,
    RTS_DURATION,
    DIFS,
    BACKOFF_MAXIMUM,
    BACKOFF_MINIMUM,
    SIFS,
)
from utils.counter import Counter


class CSMA(AbstractCSMA):
    rts_duration: int = RTS_DURATION
    cts_duration: int = CTS_DURATION
    sifs_amount: int = SIFS
    difs_amount: int = DIFS
    backoff_max: int = BACKOFF_MAXIMUM
    backoff_min: int = BACKOFF_MINIMUM
    backoff_range: int = BACKOFF_MINIMUM
    nav: Counter
    allocated: Counter
    sifs: Counter
    difs: Counter
    backoff: Counter

    def __init__(self, slot_time: int):
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
            return False

        # wait for backoff
        if self.backoff.is_left():
            if not is_busy:
                self.backoff.decrease(step)
            return False

        # check the medium then set backoff
        if is_busy:
            self.set_difs()
            self.set_backoff()
            return False

        return True
