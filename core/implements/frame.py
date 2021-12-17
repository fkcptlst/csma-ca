import random
from typing import List, Tuple, Optional

from dependency_injector.wiring import Provide
from constant import ACK_FRAME_SIZE, CTS_FRAME_SIZE, RTS_FRAME_SIZE
from core.abc.frame import AbstractFrame, AbstractFrameStorage, FrameType
from core.abc.station import AbstractStation
from core.container import DIContainer
from core.time.participant import TimeParticipant
from utils.helper import get_circle, get_distance, get_line


class FramePath(TimeParticipant):
    def __init__(self, location: Tuple[float, float]):
        self.location = location


class FrameRadius(TimeParticipant):
    def __init__(self, location: Tuple[float, float]):
        self.location = location


class FrameRadiusEdge(TimeParticipant):
    def __init__(self, location: Tuple[float, float]):
        self.location = location


class DrawRadiusMixin:
    radius: List[FrameRadius] = []
    paths: List[FramePath] = []

    def delete_radius(self):
        for radius in self.radius:
            radius.unregister()
        for path in self.paths:
            path.unregister()
        self.radius = []
        self.paths = []

    def draw_radius(self):
        radius = int(get_distance(self.location, self.sender.location))
        radius_tail = int(get_distance(self.location_tail, self.sender.location))
        for i in range(radius_tail, radius):
            for point in get_circle(self.sender.location, i):
                path = (
                    FrameRadius(point) if i != (radius - 1) else FrameRadiusEdge(point)
                )
                path.register()
                self.radius.append(path)

        paths = get_line(self.location_tail, self.location)
        for point in paths:
            path = FramePath(point)
            path.register()
            self.paths.append(path)


class Frame(AbstractFrame, DrawRadiusMixin, TimeParticipant):
    typ = "DATA"
    sent = None
    sent_done = None
    vanished = None

    def __init__(
        self,
        id: str,
        sender: AbstractStation,
        receiver: AbstractStation,
        typ: FrameType,
        size: int = Provide[DIContainer.settings.frame_size],
        duration: Optional[int] = None,
    ):
        self.id = id
        self.sender = sender
        self.receiver = receiver
        self.typ = typ

        self.size = size
        if self.typ == "RTS":
            self.size = RTS_FRAME_SIZE
        elif self.typ == "CTS":
            self.size = CTS_FRAME_SIZE
        elif self.typ == "ACK":
            self.size = ACK_FRAME_SIZE

        self.duration = duration
        self.propagation_speed = sender.medium.propagation_speed
        self.max_range = sender.detect_range

    def is_equal(self, frame: AbstractFrame) -> bool:
        return frame.id == self.id

    def depart(self):
        self.register()
        self.sender.medium.add_frame(self)
        self.sent = self.timeline.current

    def done(self):
        self.sent_done = self.timeline.current

    def vanish(self):
        self.vanished = self.timeline.current
        self.delete_radius()
        self.unregister()

    def get_location(self, moved: float) -> Tuple[float, float]:
        distance = self.distance
        if distance == 0:
            return self.sender.location
        return (
            (
                self.sender.location[0]
                + (self.receiver.location[0] - self.sender.location[0])
                * moved
                / distance
            ),
            (
                self.sender.location[1]
                + (self.receiver.location[1] - self.sender.location[1])
                * moved
                / distance
            ),
        )

    @property
    def moved_tail(self) -> float:
        if self.sent_done is None:
            return 0
        return max(
            (self.timeline.current - self.sent_done - self.timeline.step)
            * self.propagation_speed,
            0,
        )

    @property
    def moved(self) -> float:
        return min(
            (self.timeline.current - self.sent) * self.propagation_speed,
            self.max_range,
        )

    @property
    def location_tail(self) -> Tuple[float, float]:
        return self.get_location(self.moved_tail)

    @property
    def location(self) -> Tuple[float, float]:
        return self.get_location(self.moved)

    @property
    def distance(self) -> float:
        return get_distance(self.sender.location, self.receiver.location)

    @staticmethod
    def assemble(
        receiver: "AbstractStation",
        sender: "AbstractStation",
        typ: FrameType = "DATA",
        duration: Optional[int] = None,
    ) -> "Frame":
        return Frame(
            id=str(random.randint(0, 1000000)),
            receiver=receiver,
            sender=sender,
            typ=typ,
            duration=duration,
        )

    def __str__(self) -> str:
        return f"{self.typ} {self.sender.id} -> {self.receiver.id}"

    def icon(self) -> str:
        return f"█{self.typ[0]}"

    def on_tick(self, step: int):
        if not self.sent:
            return

        self.delete_radius()
        self.draw_radius()


class FrameStorage(AbstractFrameStorage):
    def __init__(self, size: int = None):
        self.frames: List[Frame] = []
        self.size = size

    def is_empty(self) -> bool:
        return len(self.frames) == 0

    def is_full(self) -> bool:
        if self.size is None:
            return False
        return len(self.frames) == self.size

    def count(self) -> int:
        return len(self.frames)

    def all(self) -> List[Frame]:
        return self.frames

    def clear(self):
        self.frames = []

    def get(self):
        try:
            return self.frames[0]
        except IndexError:
            return None

    def push(self, frame):
        if self.is_full():
            return
        self.frames.append(frame)

    def pop(self):
        try:
            return self.frames.pop(0)
        except IndexError:
            return None
