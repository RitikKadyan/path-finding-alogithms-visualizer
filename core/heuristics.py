from __future__ import annotations
import math
from typing import Tuple

Coord = Tuple[int, int]


def manhattan(a: Coord, b: Coord) -> float:
    return float(abs(a[0] - b[0]) + abs(a[1] - b[1]))


def euclidean(a: Coord, b: Coord) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def octile(a: Coord, b: Coord) -> float:
    # Octile distance for 8-neighbor grids (diagonal cost = sqrt(2))
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    F = math.sqrt(2) - 1
    return float((dx + dy) + (F) * min(dx, dy))


def zero(a: Coord, b: Coord) -> float:
    return 0.0
