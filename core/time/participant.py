from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .line import TimeLine

from dependency_injector.wiring import Provide, inject

from core.container import DIContainer


class TimeParticipant:
    @inject
    def register(self, timeline: "TimeLine" = Provide[DIContainer.timeline]):
        self.timeline = timeline
        timeline.add_participant(self)

    def unregister(self):
        self.timeline.participants.remove(self)

    @property
    def current(self) -> int:
        return self.timeline.current

    def on_tick_init(self, step: int):
        pass

    def on_tick(self, step: int):
        pass
