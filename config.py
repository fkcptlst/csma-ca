from constant import (
    MEGA,
    ONE_SECOND,
    SPEED_OF_LIGHT,
)

default_settings = {
    "star_topology": True,
    "with_rts": True,
    "propagation_speed": SPEED_OF_LIGHT / 3,
    "area_size": 80,
    "station_count": 5,
    "data_rate": 11 * MEGA,
    "frame_rate": 300,
    "detect_range": 40,
    "frame_size": 8 * 1500,
    "backoff_min": 4,
    "backoff_max": 1024,
    "interval": 0.05,
    "slot_time": 20,
    "step": 10,
    "max_time": ONE_SECOND,
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

sim_settings = {
    **default_settings,
    "step": 20,
    "interval": 0.0,
    "max_time": ONE_SECOND // 10,
    "log": False,
    "log_screen": False,
}

various_settings = []
various_settings += [{**sim_settings, **s} for s in station_count]
various_settings += [{**sim_settings, **f} for f in frame_rate]
various_settings += [{**sim_settings, **b} for b in backoff_min]
