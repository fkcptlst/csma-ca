from abc import ABC, abstractmethod
from typing import List, Type, TypedDict, Union

from core.abc.csma import AbstractCSMA
from core.abc.frame import AbstractFrame, AbstractFrameStorage, FrameType


ProceedRecord = TypedDict(
    "ProceedRecord", {"typ": FrameType, "size": int, "count": int}
)


class AbstractTransmitter(ABC):
    station_id: int
    data_rate: int
    send_frames: AbstractFrameStorage
    recv_frames: AbstractFrameStorage
    detected_frames: AbstractFrameStorage

    recv: List[ProceedRecord]
    recv_current: int
    sent: List[ProceedRecord]
    sent_current: int
    collisions: int

    last_sent_data: Union[AbstractFrame, None]
    csma: AbstractCSMA
    wasted: int
    with_rts: bool

    @abstractmethod
    def __init__(
        self,
        station_id: int,
        data_rate: int,
        send_queue_size: int,
        recv_queue_size: int,
        with_rts: bool,
        frame_storage: Type[AbstractFrameStorage],
        csma: Type[AbstractCSMA],
    ):
        pass

    @abstractmethod
    def add_recv_record(self, frame: AbstractFrame):
        """Record the information of received frame.

        bps would be calculated with the total size of received data frame.

        Parameters
        ----------
        frame : AbstractFrame
            The received frame.
        """
        pass

    @abstractmethod
    def add_sent_record(self, frame: AbstractFrame):
        """Record the information of sent frame.

        collision rate would be calculated with the total count of sent frame.

        Parameters
        ----------
        frame : AbstractFrame
            The sent frame.
        """
        pass

    # receiver methods
    @abstractmethod
    def on_receive_success(self):
        """Callback function when a frame is received successfully.

        Pop the frame from the receiving frame storage, and
        add the frame information to the received record list.

        call the on_data() / on_ack() / on_rts() / on_cts() method according to the frame type.
        """
        pass

    @abstractmethod
    def on_receive_failure(self):
        """Callback function when a frame is received unsuccessfully (most likely due to the collision).

        Pop the frame from the receiving frame storage.
        """
        pass

    @abstractmethod
    def on_timeout(self):
        """Handle the timeout for ACK or CTS.

        Considers the timeout as a collision, and increase the collision count.
        Add wasted time to the total wasted time.

        To double the backoff time range, call the ``csma.collision_occured()`` method.
        """
        pass

    @abstractmethod
    def on_detect(self, frame: AbstractFrame):
        """Handle the frame detection.

        The medium of the station will calculate the distance between the frame and the station on every tick.
        If the distance is less than the threshold, the frame will be detected and this method would be called.

        Push the frame to the detected frame storage.
        If the number of detected frames is greater than 1, it means that there is a talkover.
        Push the frame to the receiving frame storage only when the talkover is not detected.

        If the frame is RTS or CTS, every station in the range should be notified, so push the frame to the receiving frame storage.
        Else if the frame is DATA or ACK, only the receiver should be notified,
        so push the frame to the receiving frame storage only if the receiver id of frame is matched with station id of self.

        Detected frames should be initialized before every tick.

        Parameters
        ----------
        frame : AbstractFrame
            The frame which is detected.
        """
        pass

    @abstractmethod
    def talkover_detected(self) -> bool:
        """Check if the talkover is detected.

        If the number of detected frames is greater than 1, it means that there is a talkover.
        """
        pass

    @abstractmethod
    def is_medium_busy(self) -> bool:
        """Check if the medium is busy.

        If the number of detected frames is greater than 0, it means that the medium is busy.
        """
        pass

    @abstractmethod
    def is_receiving(self) -> bool:
        """True if the receiving frame storage is not empty."""
        pass

    @abstractmethod
    def proceed_recv(self, step: int):
        """Proceed receiving the frame.

        If no frames are detected, it means that the some bytes of the frame are losted (most likely due to the collision).
        Then call the ``on_receive_failure()`` method.

        Else if the talkover is detected, The transmitter can not proceed the receiving because the frame would be poluted by the talkover.

        Else if the id or detected frame is not matched with the frame id in receiving frame storage,
        ``on_receive_failure()`` method would be called because this means that the transmission of original frame is ended,
        but the receiver is still wants to receiving the frame.
        This situation could happened when some bytes of the frame are losted due to the collision,
        and the one which made the collision is detected after the original transmission is ended.

        If the frame is correctly detected, proceed the receiving with it's own data rate
        call ``on_receive_success()`` method if all bytes of frame are received.

        Parameters
        ----------
        step : int
            The number of steps to proceed.
        """
        pass

    # sender methods
    @abstractmethod
    def push(self, frame: AbstractFrame):
        """Called when the station wants to send a frame.

        Set the SIFS or DIFS counter after checking which one should be set wiht ``csma.is_difs()`` method.

        If the frame existing in the sending frame storage,
        check if the frame is for DIFS or SIFS.
        If the frame is for DIFS, priority is lower than or equal to the priority of the frame
        which is going to be added to the sending frames storage.
        In that case, pop the frame out from the sending frame storage, and push the new frame.

        Parameters
        ----------
        frame : AbstractFrame
            The frame which is going to be pushed.
        """
        pass

    @abstractmethod
    def want_to_send(self) -> bool:
        """True if the sending frame storage is not empty."""
        pass

    @abstractmethod
    def is_sending(self) -> bool:
        """True if the sent bytes of currently sending frame not equals to zero."""
        pass

    @abstractmethod
    def proceed_send(self, step: int):
        """Proceed sending the frame.

        Add the sent bytes to the sent bytes of currently sending frame with it's own data rate.
        If the sent bytes of currently sending frame larger than or equals to the size of the frame,
        Call ``frame.done()``, add the sent frame to the sent record list,
        reset the sent bytes and pop the frame from the sending frame storage.

        Parameters
        ----------
        step : int
            The number of steps to proceed.
        """
        pass

    @abstractmethod
    def send(self, step: int):
        """Start sending the frame.

        If the frame is not ACK, set timeout for ACK.
        Call ``frame.depart()`` method and ``proceed_send()`` method.

        Parameters
        ----------
        step : int
            The number of steps to proceed.
        """
        pass

    # frame handlers
    @abstractmethod
    def on_data(self, frame: AbstractFrame):
        """Handle the DATA frame.

        Set SIFS counter and push ACK frame to the sending frame storage.
        Remove the timeout.

        Parameters
        ----------
        frame : AbstractFrame
            The received DATA frame.
        """
        pass

    @abstractmethod
    def on_ack(self, frame: AbstractFrame):
        """Handle the ACK frame.

        Set DIFS counter and reset the backoff range.
        Remove the timeout.

        Parameters
        ----------
        frame : AbstractFrame
            The received ACK frame.
        """
        pass

    @abstractmethod
    def on_rts(self, frame: AbstractFrame):
        """Handle the RTS frame.

        If the receiver of frame is self, set SIFS counter and push CTS frame to the sending frame storage.
        Else, set nav counter as the duration contained in the received RTS frame.

        Parameters
        ----------
        frame : AbstractFrame
            The received RTS frame.
        """
        pass

    @abstractmethod
    def on_cts(self, frame: AbstractFrame):
        """Handle the CTS frame.

        If the receiver of frame is self, set SIFS counter and push DATA frame to the sending frame storage.
        Set allocated counter as the duration contained in the received CTS frame.
        Reset the backoff range and timeout.

        Else, set nav counter as the duration contained in the received CTS frame.

        Parameters
        ----------
        frame : AbstractFrame
            The received CTS frame.
        """
        pass

    # access control
    @abstractmethod
    def is_acked(self) -> bool:
        """True if the station is acked."""
        pass

    @abstractmethod
    def timeout_occured(self, current: int) -> bool:
        """True if the station is not acked and the timeout is expired.

        Parameters
        ----------
        current : int
            The current time.
        """
        pass

    @abstractmethod
    def okay_to_send(self, step: int) -> bool:
        """Check if the station is okay to send.

        The station must be acked,
        the medium must be idle,
        and the result of ``csma.check_and_decrease()`` method must be true.

        Parameters
        ----------
        step : int
            The number of steps to decrease the csma counters.
        """
        pass
