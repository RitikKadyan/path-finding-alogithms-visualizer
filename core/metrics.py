from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import Dict, Set, Tuple
import time


@dataclass
class Metrics:
    nodes_expanded: int = 0
    path_length: int = 0
    runtime_ms: float = 0.0
    max_open_size: int = 0
    memory_estimate_bytes: int = 0
    explored: Set[Tuple[int, int]] = field(default_factory=set)
    explored_order: Dict[Tuple[int, int], int] = field(default_factory=dict)  # coord -> step number

    def start_timer(self) -> float:
        return time.perf_counter_ns()

    def end_timer(self, start_ns: float) -> None:
        end_ns = time.perf_counter_ns()
        self.runtime_ms = (end_ns - start_ns) / 1_000_000.0

    def to_dict(self) -> Dict[str, float]:
        d = asdict(self)
        d.pop('explored', None)  # Remove set from dict for CSV
        d.pop('explored_order', None)
        return d
