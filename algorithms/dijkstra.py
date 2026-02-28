from __future__ import annotations
from typing import Tuple, List

from algorithms.astar import AStar
from core.heuristics import zero
from core.grid import Grid
from core.metrics import Metrics

Coord = Tuple[int, int]


class Dijkstra(AStar):
    def __init__(self) -> None:
        super().__init__(heuristic=zero)

    # Inherits search from AStar but with zero heuristic to behave as Dijkstra
