from dataclasses import dataclass
from collections import namedtuple

from config import DISPLAY_HEIGHT, DISPLAY_WIDTH, SCALE

Vec2f = namedtuple("Point", ["x", "y"])


def normalize(x, y) -> Vec2f:
    return Vec2f((x / DISPLAY_WIDTH * (SCALE*2)) - SCALE, ((y / DISPLAY_HEIGHT * (SCALE*2)) - SCALE)*-1)
