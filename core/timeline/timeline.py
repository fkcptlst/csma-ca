import time
from typing import Callable, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .participant import TimeParticipant

from constant import AREA_SIZE, MAX_TIME, INTERVAL, STEP
from utils.area import AreaDrawer


class TimeLine:
    def __init__(
        self,
        interval: float = INTERVAL,
        step: int = STEP,
        max_time: int = MAX_TIME,
        area_size: int = AREA_SIZE,
        notation: List[Dict] = [],
        log_screen: bool = True,
    ):
        self.current = 0
        self.step = step
        self.max_time = max_time
        self.area_size = area_size
        self.interval = interval
        self.log_screen = log_screen
        self.participants: List["TimeParticipant"] = []
        self.drawer = AreaDrawer(area_size, notation)
        self.after_tick: Optional[Callable] = None

    def tick(self):
        self.current += self.step
        for participant in self.participants:
            participant.on_tick_init(self.step)

        for participant in self.participants:
            participant.on_tick(self.step)

    def set_after_tick(self, callback: Callable[["TimeLine"], None]):
        self.after_tick = callback

    def add_participant(self, participant: "TimeParticipant"):
        self.participants.append(participant)

    def run(self):
        while self.current < self.max_time:
            self.tick()
            if self.log_screen:
                self.drawer.draw_screen(self.participants)
            if self.after_tick:
                self.after_tick(self)

            time.sleep(self.interval)
