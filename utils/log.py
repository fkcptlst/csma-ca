from constant import FRAME_SIZE, KILLO, MILLI_SECOND, ONE_SECOND
from core.implements import Station, Medium, Frame
from core.timeline import TimeLine
from utils.helper import get_progress_bar


def station_notate(station: Station):
    n = ""
    n += f"{station.id}"
    if station.transmitter.is_sending() or station.transmitter.is_receiving():
        n += "*"
    else:
        n += " "
    return n


def frame_notate(frame: Frame):
    if frame.collision:
        return "XX"
    else:
        return frame.icon()


def logger_factory(medium: Medium, rts_cts: bool = True):
    def logger(timeline: TimeLine):
        processed = 0
        processed_data = 0
        collisions = 0
        sent = 0
        frame_rate = 0
        count = 0
        for station in medium.stations:
            processed += station.transmitter.received
            processed_data += station.transmitter.received_data
            collisions += station.transmitter.collisions
            sent += station.transmitter.sent // FRAME_SIZE
            frame_rate += station.frame_rate

            count += 1

        frame_rate /= count
        processed_ideal = frame_rate * FRAME_SIZE * timeline.current / ONE_SECOND

        bps_unit = KILLO
        bps = 8 * processed * ONE_SECOND / (timeline.current * bps_unit)
        data_bps = 8 * processed_data * ONE_SECOND / (timeline.current * bps_unit)
        max_bps = 8 * processed_ideal * ONE_SECOND / (timeline.current * bps_unit)
        wasted_time = (processed_ideal - processed) / (frame_rate * FRAME_SIZE)
        wasted_time_pure = (processed_ideal - processed_data) / (
            frame_rate * FRAME_SIZE
        )
        collision_rate = collisions / (sent if sent != 0 else 1)

        msg = f"{'[time]':20}{timeline.current/MILLI_SECOND:.2f}ms\n"
        msg += "\n"
        msg += f"{'[wasted]':20}{wasted_time/MILLI_SECOND:.2f}ms\n"
        msg += f"{'[throughput]':20}{bps:.2f} kbps\n"
        msg += f"{'[throughput rate]':20}{get_progress_bar(bps/max_bps)} {bps:.2f}/{max_bps:.2f} \n"
        msg += "\n"
        if rts_cts:
            msg += f"{'[wasted]':20}{wasted_time_pure/MILLI_SECOND:.2f}ms\n"
            msg += f"{'[throughput]':20}{data_bps:.2f} kbps\n"
            msg += f"{'[throughput rate]':20}{get_progress_bar(data_bps/max_bps)} {data_bps:.2f}/{max_bps:.2f} \n"
        msg += "\n"
        msg += f"{'[collision rate]':20}{get_progress_bar(collision_rate)} {collisions}/{sent}\n"
        msg += f"{'[on air frames]':20} {medium.frame_count()}\n"

        msg += "\n"
        msg += f"[node details]\n"
        msg += f"{'ID'.rjust(4)} | {'send-queue'.rjust(12)} | {'recv-queue'.rjust(12)} | {'col'.rjust(3)} | {'sending'.rjust(30)} | {'receiving'.rjust(30)} | {'detected'.rjust(12)} | {'backoff'.rjust(8)} | {'difs'.rjust(8)} | {'sifs'.rjust(8)} | {'timeout'.rjust(8)} | {'nav'.rjust(8)} | {'allocate'.rjust(8)} | "

        msg += "\n"
        for station in medium.stations:
            msg += f"[{station.id:2}] | "

            queue = ""
            for frame in station.transmitter.send_frames.all():
                if len(queue) >= 12:
                    break
                queue += f"{frame.icon()}"
            msg += f"{queue.ljust(12, '░')} | "

            queue = ""
            for frame in station.transmitter.recv_frames.all():
                if len(queue) >= 12:
                    break
                queue += f"{frame.icon()}"

            msg += f"{queue.ljust(12, '░')} | "

            msg += f"{station.transmitter.collisions:-3} | "

            sending = ""
            if station.transmitter.is_sending():
                sending = get_progress_bar(
                    station.transmitter.sent_current
                    / station.transmitter.send_frames.get().size
                )
            msg += f"{sending.ljust(30, ' ')} | "

            receiving = ""
            if station.transmitter.is_receiving():
                receiving = get_progress_bar(
                    station.transmitter.received_current
                    / station.transmitter.recv_frames.get().size
                )
            msg += f"{receiving.ljust(30, ' ')} | "

            detected = ""
            if station.transmitter.detected:
                detected = str(station.transmitter.detected)
            msg += f"{detected.rjust(12, ' ')} | "

            msg += f"{station.transmitter.csma.backoff.value:-8} | "
            msg += f"{station.transmitter.csma.difs.value:-8} | "
            msg += f"{station.transmitter.csma.sifs.value:-8} | "

            timeout = ""
            if station.transmitter.last_sent:
                timeout = str(
                    station.timeout
                    - (timeline.current - station.transmitter.last_sent.sent)
                )
            msg += f"{timeout.rjust(8)} | "

            nav = ""
            if station.transmitter.csma.nav.value:
                nav = str(station.transmitter.csma.nav.value)
            msg += f"{nav.rjust(8)} | "

            allocated = ""
            if station.transmitter.csma.allocated.value:
                allocated = str(station.transmitter.csma.allocated.value)
            msg += f"{allocated.rjust(8)} | "

            msg += f"\n"

        msg += "\n"
        print(msg)

    return logger
