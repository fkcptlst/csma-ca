import json
from typing import Dict
from constant import KILLO, MILLI_SECOND, ONE_SECOND
from core.implements import Station, Medium, Frame
from core.time.line import TimeLine
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


def get_log(timeline: TimeLine, medium: Medium, frame_size: int, verbose: bool):
    processed = 0
    collisions = 0
    sent = 0
    data_rate = 0
    frame_rate = 0
    count = 0
    wasted = 0
    for station in medium.stations:
        processed += sum(
            [r["size"] for r in station.transmitter.recv if r["typ"] == "DATA"]
        )
        collisions += station.transmitter.collisions
        wasted += station.transmitter.wasted
        sent += sum([r["count"] for r in station.transmitter.sent])
        data_rate += station.data_rate
        frame_rate += station.frame_rate

        count += 1

    data_rate /= count
    frame_rate /= count
    processed_ideal = (
        frame_size
        * (frame_rate / ONE_SECOND)
        * (data_rate / ONE_SECOND)
        * timeline.current
    )

    bps_unit = KILLO
    bps = 8 * processed * ONE_SECOND / (timeline.current * bps_unit)
    max_bps = 8 * processed_ideal * ONE_SECOND / (timeline.current * bps_unit)
    collision_rate = collisions / (sent if sent != 0 else 1)

    msg = f"{'[time]':20}{timeline.current/MILLI_SECOND:.2f}ms\n"
    msg += "\n"
    msg += f"{'[wasted]':20}{wasted/MILLI_SECOND:.2f}ms\n"
    msg += f"{'[throughput]':20}{bps:.2f} kbps\n"
    msg += f"{'[throughput rate]':20}{get_progress_bar(bps/max_bps)} {bps:.2f}/{max_bps:.2f} \n"
    msg += "\n"
    msg += f"{'[collision rate]':20}{get_progress_bar(collision_rate)} {collisions}/{sent}\n"
    if verbose:
        msg += f"{'[frames on air]':20} {medium.frame_count()}\n"

    msg += "\n"
    msg += f"[node details]\n"
    msg += f"{'ID'.rjust(4)} | {'s'.rjust(3)} | {'r'.rjust(3)} | {'c'.rjust(3)} | "
    if verbose:
        msg += f"{'send'.rjust(8)} | {'recv'.rjust(8)} | {'sending'.rjust(30)} | {'receiving'.rjust(30)} | {'detected'.rjust(12)} | {'bo max'.rjust(8)} | {'backoff'.rjust(8)} | {'difs'.rjust(8)} | {'sifs'.rjust(8)} | {'timeout'.rjust(8)} | {'nav'.rjust(8)} | {'allocate'.rjust(8)} | "

    msg += "\n"
    for station in medium.stations:
        msg += f"[{station.id:2}] | "
        msg += f"{sum([r['count'] for r in station.transmitter.sent]):-3} | "
        msg += f"{sum([r['count'] for r in station.transmitter.recv]):-3} | "
        msg += f"{station.transmitter.collisions:-3} | "

        if verbose:
            queue = ""
            for frame in station.transmitter.send_frames.all():
                if len(queue) >= 8:
                    break
                queue += f"{frame.icon()}"
            msg += f"{queue.ljust(8, '░')} | "

            queue = ""
            for frame in station.transmitter.recv_frames.all():
                if len(queue) >= 8:
                    break
                queue += f"{frame.icon()}"

            msg += f"{queue.ljust(8, '░')} | "

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
                    station.transmitter.recv_current
                    / station.transmitter.recv_frames.get().size
                )
            msg += f"{receiving.ljust(30, ' ')} | "

            detected = ""
            if station.transmitter.detected_frames.get():
                if station.transmitter.detected_frames.count() > 1:
                    detected += "*"
                detected += str(station.transmitter.detected_frames.get())
            msg += f"{detected.rjust(12, ' ')} | "

            msg += f"{(station.transmitter.csma.backoff_range-1):-8} | "
            msg += f"{station.transmitter.csma.backoff.value:-8} | "
            msg += f"{station.transmitter.csma.difs.value:-8} | "
            msg += f"{station.transmitter.csma.sifs.value:-8} | "

            timeout = ""
            if station.transmitter.last_sent:
                timeout = str(
                    station.transmitter.timeout
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
    return msg


def logger_factory(medium: Medium, frame_size: int):
    def logger(timeline: TimeLine):
        print(get_log(timeline, medium, frame_size, True))

    return logger


def summary_settings(settings: Dict):
    summary = ""
    summary += f"{settings['station_count']}_stations_"
    summary += f"{settings['frame_rate']}_fps_"
    summary += f"{settings['backoff_min']}_backoff"
    return summary


def log_result(timeline: TimeLine, settings: Dict):
    mediums = [p for p in timeline.participants if isinstance(p, Medium)]
    if len(mediums) != 1:
        raise ValueError("Only one medium is supported")
    medium = mediums[0]
    frame_size = settings["frame_size"]

    msg = get_log(timeline, medium, frame_size, False)
    with open(f"results/{summary_settings(settings)}.txt", "w") as f:
        f.write(msg)
