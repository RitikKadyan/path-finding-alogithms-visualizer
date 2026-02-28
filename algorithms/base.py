from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Tuple
from core.metrics import Metrics
from core.grid import Grid

Coord = Tuple[int, int]


class Algorithm(ABC):
    """Base algorithm interface. Implementations should not rely on global state."""

    @abstractmethod
    def search(self, grid: Grid, start: Coord, goal: Coord) -> Tuple[List[Coord], Metrics]:
        """Return path (list of coords from start to goal inclusive) and Metrics."""
