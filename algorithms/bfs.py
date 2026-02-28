from __future__ import annotations
from collections import deque
from typing import Dict, List, Tuple

from algorithms.base import Algorithm
from core.grid import Grid
from core.metrics import Metrics

Coord = Tuple[int, int]


class BFS(Algorithm):
    def search(self, grid: Grid, start: Coord, goal: Coord) -> Tuple[List[Coord], Metrics]:
        start_ns = Metrics().start_timer()
        metrics = Metrics()
        step_counter = [0]

        q = deque([start])
        parents: Dict[Coord, Coord] = {}
        visited = {start}

        while q:
            current = q.popleft()
            metrics.nodes_expanded += 1
            metrics.explored.add(current)
            metrics.explored_order[current] = step_counter[0]
            step_counter[0] += 1
            
            if current == goal:
                path: List[Coord] = []
                node = current
                while True:
                    path.append(node)
                    if node == start:
                        break
                    node = parents[node]
                path.reverse()
                metrics.path_length = len(path)
                metrics.end_timer(start_ns)
                return path, metrics

            for nb in grid.neighbors(current):
                if nb not in visited:
                    visited.add(nb)
                    parents[nb] = current
                    q.append(nb)
                    metrics.max_open_size = max(metrics.max_open_size, len(q))

        metrics.end_timer(start_ns)
        return [], metrics
