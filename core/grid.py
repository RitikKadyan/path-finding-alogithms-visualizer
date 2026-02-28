from __future__ import annotations
from typing import Dict, Iterable, List, Set, Tuple


Coord = Tuple[int, int]


class Grid:
    """Grid graph with O(1) neighbor generation using direction vectors.

    Stores optional per-cell weights and blocked cells. Neighbors are computed
    from integer offsets so no O(V^2) neighbor construction is necessary.
    """

    def __init__(self, rows: int, cols: int, diagonal: bool = False) -> None:
        self.rows = rows
        self.cols = cols
        self.diagonal = diagonal
        self.weights: Dict[Coord, float] = {}
        self.blocks: Set[Coord] = set()

        # 4-directional by default
        self._dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        # 8-directional includes diagonals
        self._dirs8 = self._dirs4 + [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    @property
    def directions(self) -> List[Coord]:
        return self._dirs8 if self.diagonal else self._dirs4

    def in_bounds(self, coord: Coord) -> bool:
        r, c = coord
        return 0 <= r < self.rows and 0 <= c < self.cols

    def passable(self, coord: Coord) -> bool:
        return coord not in self.blocks

    def neighbors(self, coord: Coord) -> Iterable[Coord]:
        r, c = coord
        for dr, dc in self.directions:
            nb = (r + dr, c + dc)
            if self.in_bounds(nb) and self.passable(nb):
                yield nb

    def set_weight(self, coord: Coord, weight: float) -> None:
        if not self.in_bounds(coord):
            raise IndexError("coord out of bounds")
        if weight <= 0:
            raise ValueError("weight must be positive")
        self.weights[coord] = float(weight)

    def get_cost(self, from_coord: Coord, to_coord: Coord) -> float:
        # By default cost is the weight of the target cell (common convention)
        return self.weights.get(to_coord, 1.0)

    def add_block(self, coord: Coord) -> None:
        if self.in_bounds(coord):
            self.blocks.add(coord)

    def remove_block(self, coord: Coord) -> None:
        self.blocks.discard(coord)

    def randomize_blocks(self, density: float, rng) -> None:
        # rng is expected to be random.Random or similar with .random() and .randint
        import math

        self.blocks.clear()
        for r in range(self.rows):
            for c in range(self.cols):
                if rng.random() < density:
                    self.blocks.add((r, c))
