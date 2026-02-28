from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Node:
    """Lightweight node representation.

    Immutable value object used by the engine when needed. Algorithms operate on
    coordinate tuples (row, col) for performance, but this class is helpful for
    higher-level APIs and clarity.
    """

    row: int
    col: int
    weight: float = 1.0

    def to_tuple(self) -> Tuple[int, int]:
        return (self.row, self.col)

    def __repr__(self) -> str:
        return f"Node(r={self.row},c={self.col},w={self.weight})"
