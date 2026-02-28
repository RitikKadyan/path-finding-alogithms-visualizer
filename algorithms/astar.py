from __future__ import annotations
import heapq
import itertools
from typing import Dict, List, Tuple

from algorithms.base import Algorithm
from core.metrics import Metrics
from core.grid import Grid
from core.heuristics import manhattan

Coord = Tuple[int, int]


class AStar(Algorithm):
    def __init__(self, heuristic=manhattan):
        self.heuristic = heuristic

    def search(self, grid: Grid, start: Coord, goal: Coord) -> Tuple[List[Coord], Metrics]:
        start_ns = Metrics().start_timer()
        metrics = Metrics()
        step_counter = [0]  # Use list to allow increment in nested scope

        open_heap: List[Tuple[float, int, Coord]] = []
        counter = itertools.count()
        g_score: Dict[Coord, float] = {start: 0.0}
        parents: Dict[Coord, Coord] = {}

        f0 = self.heuristic(start, goal)
        heapq.heappush(open_heap, (f0, next(counter), start))

        open_set = {start}

        while open_heap:
            metrics.max_open_size = max(metrics.max_open_size, len(open_heap))
            _, _, current = heapq.heappop(open_heap)
            open_set.discard(current)

            if current == goal:
                # reconstruct
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

            metrics.nodes_expanded += 1
            metrics.explored.add(current)
            metrics.explored_order[current] = step_counter[0]
            step_counter[0] += 1

            for neighbor in grid.neighbors(current):
                tentative_g = g_score[current] + grid.get_cost(current, neighbor)
                if tentative_g < g_score.get(neighbor, float('inf')):
                    parents[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + self.heuristic(neighbor, goal)
                    if neighbor not in open_set:
                        heapq.heappush(open_heap, (f, next(counter), neighbor))
                        open_set.add(neighbor)

        metrics.end_timer(start_ns)
        return [], metrics
