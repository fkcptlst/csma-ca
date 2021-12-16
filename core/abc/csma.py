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
        """Handle the collision.

        Set backoff range to min of backoff range * 2 and the maximum backoff time.
        """
        pass

    @abstractmethod
    def reset_backoff_range(self):
        """Set the backoff range to the minimum backoff time."""
        pass

    @abstractmethod
    def set_backoff(self):
        """Set the backoff time randomly with the backoff range."""
        pass

    @abstractmethod
    def set_sifs(self):
        """Set the SIFS time."""
        pass

    @abstractmethod
    def set_difs(self):
        """Set the DIFS time."""
        pass

    @abstractmethod
    def set_nav(self, duration: int):
        """Set the NAV time for hibernation.

        Parameters
        ----------
        duration : int
            The duration of the NAV time.
        """
        pass

    @abstractmethod
    def set_allocated(self, duration: int):
        """Set the allocated time.

        Parameters
        ----------
        duration : int
            The duration of the allocated time.
        """
        pass

    @abstractmethod
    def is_difs(self, with_rts: bool, frame: AbstractFrame):
        """Check if the frame should be sent after DIFS counter.

        if with_rts is True, return True if the frame is a RTS frame.
        Else, return True if the frame is a DATA frame.

        Parameters
        ----------
        with_rts : bool
            Current simulation is with RTS.
        frame : AbstractFrame
            The frame to check.
        """
        pass

    @abstractmethod
    def nav_decrease(self, step: int):
        """Decrease the NAV counter.

        decrease the NAV or allocated counter if there is remaining.

        Parameters
        ----------
        step : int
            The step to decrease the counter.
        """
        pass

    @abstractmethod
    def check_and_decrease(self, is_busy: bool, step: int):
        """Access control and decrement of the counters.

        If NAV is not expired, return False.
        Decrement of the NAV counter must be done in the station for every tick. It is separated because this method is not called in every tick.

        If SIFS or DIFS is not expired, return False and decrease them.
        If DIFS is just ended, set the backoff counter before the returning.

        If backoff is not expired, return False.
        Before returning, decrease the backoff counter if the medium is not busy.
        If busy, remove the backoff and set DIFS counter. This sets the state of the station to start of the state diagram.

        If every counter is expired, return True if the medium is not busy.
        If busy, set DIFS and backoff counter.


        Parameters
        ----------
        is_busy : bool
            True if the channel is busy.
        step : int
            The step to decrease the counter.
        """
        pass
