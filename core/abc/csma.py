from abc import ABC, abstractmethod
from core.abc.frame import AbstractFrame
from utils.counter import Counter


class AbstractCSMA(ABC):
    rts_duration: int
    cts_duration: int
    sifs_amount: int
    difs_amount: int
    backoff_max: int
    backoff_min: int
    backoff_range: int
    frame_time: int
    nav: Counter
    allocated: Counter
    sifs: Counter
    difs: Counter
    backoff: Counter

    @abstractmethod
    def __init__(self, slot_time: int, backoff_min: int, backoff_max: int):
        pass

    @abstractmethod
    def collision_occured(self):
        pass

    @abstractmethod
    def reset_backoff_range(self):
        pass

    @abstractmethod
    def set_backoff(self):
        pass

    @abstractmethod
    def set_sifs(self):
        pass

    @abstractmethod
    def set_difs(self):
        pass

    @abstractmethod
    def set_nav(self, duration: int):
        pass

    @abstractmethod
    def set_allocated(self, duration: int):
        pass

    @abstractmethod
    def is_difs(self, with_rts: bool, frame: AbstractFrame):
        pass

    @abstractmethod
    def nav_decrease(self, step: int):
        pass

    @abstractmethod
    def check_and_decrease(self, is_busy: bool, step: int):
        pass
