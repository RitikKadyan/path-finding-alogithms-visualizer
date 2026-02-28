from __future__ import annotations
from typing import Iterable, Tuple
import pygame

Coord = Tuple[int, int]


class Renderer:
    """Simple Pygame renderer for the grid and pathfinding instrumentation.

    Keeps rendering code separated from algorithm logic.
    """

    COLORS = {
        'bg': (20, 20, 20),
        'grid': (40, 40, 40),
        'block': (80, 80, 80),
        'start': (255, 215, 0),
        'goal': (255, 0, 0),
        'open': (56, 228, 174),
        'closed': (100, 100, 255),
        'path': (200, 200, 30),
    }

    def __init__(self, grid_rows: int, grid_cols: int, cell_size: int = 20, margin: int = 1):
        pygame.init()
        self.cell_size = cell_size
        self.margin = margin
        self.rows = grid_rows
        self.cols = grid_cols
        w = grid_cols * (cell_size + margin) + margin
        h = grid_rows * (cell_size + margin) + margin + 80
        self.screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption('Pathfinding Engine')
        self.font = pygame.font.SysFont('Consolas', 18)
        self.clock = pygame.time.Clock()

    def draw_grid(self, grid, start: Coord = None, goal: Coord = None,
                  open_set: Iterable[Coord] = (), closed_set: Iterable[Coord] = (), path: Iterable[Coord] = ()):  # pragma: no cover - UI
        self.screen.fill(self.COLORS['bg'])

        for r in range(self.rows):
            for c in range(self.cols):
                rect = pygame.Rect(self.margin + c * (self.cell_size + self.margin),
                                   self.margin + r * (self.cell_size + self.margin),
                                   self.cell_size, self.cell_size)
                coord = (r, c)
                if coord in getattr(grid, 'blocks', set()):
                    color = self.COLORS['block']
                else:
                    color = self.COLORS['grid']
                pygame.draw.rect(self.screen, color, rect)

        for coord in open_set:
            self._draw_cell(coord, self.COLORS['open'])
        for coord in closed_set:
            self._draw_cell(coord, self.COLORS['closed'])
        for coord in path:
            self._draw_cell(coord, self.COLORS['path'])

        if start:
            self._draw_cell(start, self.COLORS['start'])
        if goal:
            self._draw_cell(goal, self.COLORS['goal'])

        pygame.display.flip()

    def _draw_cell(self, coord: Coord, color: Tuple[int, int, int]):
        r, c = coord
        rect = pygame.Rect(self.margin + c * (self.cell_size + self.margin),
                           self.margin + r * (self.cell_size + self.margin),
                           self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, color, rect)

    def draw_metrics(self, metrics):  # pragma: no cover - UI
        lines = [f"nodes: {metrics.nodes_expanded}", f"len: {metrics.path_length}",
                 f"ms: {metrics.runtime_ms:.2f}", f"max_open: {metrics.max_open_size}"]
        x = 10
        y = self.rows * (self.cell_size + self.margin) + 10
        for line in lines:
            surf = self.font.render(line, True, (230, 230, 230))
            self.screen.blit(surf, (x, y))
            y += 20

    def tick(self, fps: int = 30):  # pragma: no cover - UI
        self.clock.tick(fps)
