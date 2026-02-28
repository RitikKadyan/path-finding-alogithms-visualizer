from __future__ import annotations
import argparse
import csv
import random
import time
from typing import List, Tuple

from core.grid import Grid
from algorithms.astar import AStar
from algorithms.dijkstra import Dijkstra
from algorithms.bfs import BFS
from algorithms.bidirectional import BidirectionalBFS
from core.heuristics import manhattan, euclidean, octile

Coord = Tuple[int, int]


ALGS = {
    'astar': AStar(manhattan),
    'astar_euclid': AStar(euclidean),
    'dijkstra': Dijkstra(),
    'bfs': BFS(),
    'bidir': BidirectionalBFS(),
}


def run_once(rows: int, cols: int, density: float, alg_name: str, seed: int) -> dict:
    rng = random.Random(seed)
    grid = Grid(rows, cols, diagonal=False)
    grid.randomize_blocks(density, rng)
    start = (0, 0)
    goal = (rows - 1, cols - 1)

    alg = ALGS[alg_name]
    start_time = time.perf_counter()
    path, metrics = alg.search(grid, start, goal)
    elapsed = (time.perf_counter() - start_time) * 1000.0
    result = metrics.to_dict()
    result.update({'alg': alg_name, 'rows': rows, 'cols': cols, 'density': density, 'seed': seed, 'wall_time_ms': elapsed})
    return result


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rows', type=int, default=50)
    parser.add_argument('--cols', type=int, default=50)
    parser.add_argument('--density', type=float, default=0.2)
    parser.add_argument('--runs', type=int, default=5)
    parser.add_argument('--out', type=str, default='benchmarks.csv')
    args = parser.parse_args()

    rows, cols = args.rows, args.cols
    density = args.density
    runs = args.runs

    rows_out: List[dict] = []
    seeds = [int(time.time()) + i for i in range(runs)]
    for alg in ALGS:
        for i, seed in enumerate(seeds):
            res = run_once(rows, cols, density, alg, seed)
            rows_out.append(res)
            print(f"{alg} run {i+1}/{runs}: nodes={res['nodes_expanded']} ms={res['runtime_ms']:.2f} pathlen={res['path_length']}")

    # write CSV
    keys = sorted(rows_out[0].keys()) if rows_out else []
    with open(args.out, 'w', newline='') as fh:
        writer = csv.DictWriter(fh, keys)
        writer.writeheader()
        writer.writerows(rows_out)
    print(f"Wrote {len(rows_out)} rows to {args.out}")


if __name__ == '__main__':
    cli()
