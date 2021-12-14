from abc import ABC, abstractmethod
from typing import Optional, Union, Literal
from typing import TYPE_CHECKING, List, Tuple

if TYPE_CHECKING:
    from .station import AbstractStation


FrameType = Union[Literal["DATA"], Literal["ACK"], Literal["RTS"], Literal["CTS"]]


class AbstractFrame(ABC):
    id: str
    typ: FrameType
    sender: "AbstractStation"
    receiver: "AbstractStation"
    duration: Optional[int]

    max_range: int
    size: int

    sent: Optional[int]
    sent_done: Optional[int]
    vanished: Optional[int]

    collision: bool

    is_duplicate: bool

    # department and arrival
    @abstractmethod
    def depart(self):
        pass

    @abstractmethod
    def done(self):
        pass

    @abstractmethod
    def vanish(self):
        pass

    @abstractmethod
    def collide(self):
        pass

    # locations
    @property
    @abstractmethod
    def moved(self) -> float:
        pass

    @property
    @abstractmethod
    def location(self) -> Tuple[int, int]:
        pass

    @property
    @abstractmethod
    def distance(self) -> float:
        pass

    # frame properties
    @staticmethod
    @abstractmethod
    def assemble(
        receiver: "AbstractStation",
        sender: "AbstractStation",
        typ: FrameType = "DATA",
        duration: Union[int, None] = None,
    ) -> "AbstractFrame":
        pass

    @abstractmethod
    def duplicate(self) -> "AbstractFrame":
        pass

    @abstractmethod
    def is_equal(self, frame: "AbstractFrame") -> bool:
        pass

    @abstractmethod
    def icon(self) -> str:
        pass


class AbstractFrameStorage(ABC):
    frames: List[AbstractFrame] = []
    size: int

    @abstractmethod
    def is_empty(self) -> bool:
        pass

    @abstractmethod
    def is_full(self) -> bool:
        pass

    @abstractmethod
    def count(self) -> int:
        pass

    @abstractmethod
    def all(self) -> List[AbstractFrame]:
        pass

    @abstractmethod
    def get(self) -> Union[AbstractFrame, None]:
        pass

    @abstractmethod
    def push(self, frame) -> None:
        pass

    @abstractmethod
    def pop(self) -> Union[AbstractFrame, None]:
        pass
