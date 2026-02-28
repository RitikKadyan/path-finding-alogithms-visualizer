from __future__ import annotations
from typing import Tuple

Coord = Tuple[int, int]


class Controls:
    """Simple input helper. Keeps UI input handling separated for testability.

    In a real app this would be richer (drag to paint, adjustable brush, etc.).
    """

    def __init__(self):
        pass

    @staticmethod
    def mouse_to_cell(mouse_pos: Tuple[int, int], cell_size: int, margin: int) -> Coord:
        x, y = mouse_pos
        col = x // (cell_size + margin)
        row = y // (cell_size + margin)
        return row, col
