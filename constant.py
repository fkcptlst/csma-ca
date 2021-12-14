import os
from dotenv import load_dotenv

load_dotenv("config.env")

INTERVAL = float(os.getenv("TIMELINE_INTERVAL", 0.05))  # seconds
AREA_SIZE = int(os.getenv("AREA_SIZE", 50))  # km

FRAME_SIZE = int(os.getenv("FRAME_SIZE", 1500))  # Bytes
FRAME_RATE = int(os.getenv("FRAME_RATE", 500))  # Frames/s

STATION_DETECT_RANGE = int(os.getenv("STATION_DETECT_RANGE", 25))  # km
STATION_COUNT = int(os.getenv("STATION_COUNT", 10))
STATION_FRAME_PROBABILITY = float(os.getenv("STATION_FRAME_PROBABILITY", 0.05))

BACKOFF_MINIMUM = int(os.getenv("BACKOFF_MINIMUM", 4))
BACKOFF_MAXIMUM = int(os.getenv("BACKOFF_MAXIMUM", 1024))

STAR_TOPOLOGY = bool(os.getenv("STAR_TOPOLOGY", False))
USE_RTS_CTS = bool(os.getenv("USE_RTS_CTS", False))

ONE_SECOND = 1000000  # micro seconds
MILLI_SECOND = 1000
MAX_TIME = ONE_SECOND

KILLO = 1000
MEGA = 1000000

SPEED_OF_LIGHT = 0.3
PROPAGATION_SPEED = SPEED_OF_LIGHT / 3

# SLOT_TIME must be divisible by STEP
exact_slot_time = int(STATION_DETECT_RANGE / PROPAGATION_SPEED)
divider = 10
SLOT_TIME = int(exact_slot_time / divider) * divider  # 250
STEP = int(SLOT_TIME / divider)  # 25

SIFS = SLOT_TIME
DIFS = SIFS + 2 * SLOT_TIME

FRAME_TIME = int(ONE_SECOND / FRAME_RATE + 2 * SLOT_TIME)
RTS_DURATION = SIFS + FRAME_TIME + SIFS + FRAME_TIME + SIFS + FRAME_TIME
CTS_DURATION = SIFS + FRAME_TIME + SIFS + FRAME_TIME

ACK_TIMEOUT = SIFS + 2 * FRAME_TIME
CTS_TIMEOUT = SIFS + 2 * FRAME_TIME
