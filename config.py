from constant import (
    MEGA,
    ONE_SECOND,
    SPEED_OF_LIGHT,
)

default_settings = {
    "star_topology": True,
    "with_rts": True,
    "propagation_speed": SPEED_OF_LIGHT / 3,
    "area_size": 50,
    "station_count": 5,
    "data_rate": 11 * MEGA,
    "frame_rate": 500,
    "detect_range": 25,
    "frame_size": 8 * 1500,
    "backoff_min": 2,
    "backoff_max": 1024,
    "interval": 0.0,
    "slot_time": 20,
    "step": 10,
    "max_time": ONE_SECOND // 1000,
    "area_size": 50,
    "log": True,
    "log_screen": True,
    "sifs": 10,
}

station_count = [
    {"station_count": 3},
    {"station_count": 10},
    {"station_count": 15},
    {"station_count": 20},
    {"station_count": 30},
    {"station_count": 50},
]

backoff_min = [
    {"backoff_min": 2},
    {"backoff_min": 4},
    {"backoff_min": 8},
    {"backoff_min": 16},
    {"backoff_min": 32},
    {"backoff_min": 128},
]

frame_rate = [
    {"frame_rate": 100},
    {"frame_rate": 200},
    {"frame_rate": 300},
    {"frame_rate": 400},
    {"frame_rate": 500},
]

various_settings = [
    {**default_settings, **s, **b, **f, "log": False, "log_screen": False}
    for s in station_count
    for b in backoff_min
    for f in frame_rate
]
