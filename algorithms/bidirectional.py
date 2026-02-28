from __future__ import annotations
from collections import deque
from typing import Dict, List, Tuple, Optional

from algorithms.base import Algorithm
from core.grid import Grid
from core.metrics import Metrics

Coord = Tuple[int, int]


class BidirectionalBFS(Algorithm):
    def search(self, grid: Grid, start: Coord, goal: Coord) -> Tuple[List[Coord], Metrics]:
        start_ns = Metrics().start_timer()
        metrics = Metrics()
        step_counter = [0]

        if start == goal:
            metrics.path_length = 1
            metrics.explored.add(start)
            metrics.explored_order[start] = 0
            metrics.end_timer(start_ns)
            return [start], metrics

        q_f = deque([start])
        q_b = deque([goal])
        parents_f: Dict[Coord, Coord] = {}
        parents_b: Dict[Coord, Coord] = {}
        seen_f = {start}
        seen_b = {goal}

        meeting: Optional[Coord] = None

        while q_f and q_b:
            metrics.max_open_size = max(metrics.max_open_size, len(q_f) + len(q_b))

            # forward step
            for _ in range(len(q_f)):
                cur = q_f.popleft()
                metrics.nodes_expanded += 1
                metrics.explored.add(cur)
                metrics.explored_order[cur] = step_counter[0]
                step_counter[0] += 1
                for nb in grid.neighbors(cur):
                    if nb in seen_b:
                        meeting = nb
                        parents_f[nb] = cur
                        break
                    if nb not in seen_f:
                        seen_f.add(nb)
                        parents_f[nb] = cur
                        q_f.append(nb)
                if meeting:
                    break
            if meeting:
                break

            # backward step
            for _ in range(len(q_b)):
                cur = q_b.popleft()
                metrics.nodes_expanded += 1
                metrics.explored.add(cur)
                metrics.explored_order[cur] = step_counter[0]
                step_counter[0] += 1
                for nb in grid.neighbors(cur):
                    if nb in seen_f:
                        meeting = nb
                        parents_b[nb] = cur
                        break
                    if nb not in seen_b:
                        seen_b.add(nb)
                        parents_b[nb] = cur
                        q_b.append(nb)
                if meeting:
                    break
            if meeting:
                break

        if meeting is None:
            metrics.end_timer(start_ns)
            return [], metrics

        # Reconstruct path from start -> meeting -> goal
        path_f: List[Coord] = []
        node = meeting
        while node != start:
            path_f.append(node)
            node = parents_f[node]
        path_f.append(start)
        path_f.reverse()

        path_b: List[Coord] = []
        node = meeting
        while node != goal:
            node = parents_b.get(node, node)
            path_b.append(node)

        path = path_f + path_b
        metrics.path_length = len(path)
        metrics.end_timer(start_ns)
        return path, metrics
