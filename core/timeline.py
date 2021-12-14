import time
from typing import Callable, Dict, List, Optional
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
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


class TimeLineContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    timeline = providers.Singleton(
        TimeLine,
        notation=config.notation,
        log_screen=config.log_screen,
        step=config.step,
    )


class TimeParticipant:
    @inject
    def register(self, timeline: TimeLine = Provide[TimeLineContainer.timeline]):
        self.timeline = timeline
        timeline.add_participant(self)

    def unregister(self):
        self.timeline.participants.remove(self)
        self.timeline = None

    @property
    def current(self) -> int:
        return self.timeline.current

    def on_tick_init(self, step: int):
        pass

    def on_tick(self, step: int):
        pass
