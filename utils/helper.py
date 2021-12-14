import os
from random import randint
from typing import Tuple
import math


def is_location_equal(l1: Tuple[int, int], l2: Tuple[int, int]) -> bool:
    return get_distance(l1, l2) < 1.5


def get_distance(l1: Tuple[float, float], l2: Tuple[float, float]) -> float:
    return math.sqrt((l1[0] - l2[0]) ** 2 + (l1[1] - l2[1]) ** 2)


def get_random_location(area_size: int, radius: int = None) -> Tuple[int, int]:
    l = (randint(0, area_size), randint(0, area_size))
    if radius is not None:
        center = (area_size // 2, area_size // 2)
        while get_distance(l, center) > radius:
            l = (randint(0, area_size), randint(0, area_size))
    return l


def get_line(l1: Tuple[float, float], l2: Tuple[float, float]):
    n = int(get_distance(l1, l2))
    return [
        (
            l1[0] + (l2[0] - l1[0]) * x / n,
            l1[1] + (l2[1] - l1[1]) * x / n,
        )
        for x in range(0, n)
    ]


# https://stackoverflow.com/questions/8487893/generate-all-the-points-on-the-circumference-of-a-circle
def get_circle(center: Tuple[float, float], r: float):
    pi = math.pi
    n = int(2 * r * pi)
    return [
        (
            center[0] + math.cos(2 * pi * (x / n)) * r,
            center[1] + math.sin(2 * pi * (x / n)) * r,
        )
        for x in range(0, n)
    ]


def screen_clear():
    if os.name == "posix":
        _ = os.system("clear")
    else:
        _ = os.system("cls")


def get_progress_bar(progress: float, show_percentage: bool = True) -> str:
    unit = 20
    percent = int(progress * unit)
    progress_bar = ""
    for _ in range(0, min(percent, unit)):
        progress_bar += "█"
    for _ in range(percent, unit):
        progress_bar += "░"
    if show_percentage:
        progress_bar += f" {(progress * 100):.2f}%"

    return progress_bar
