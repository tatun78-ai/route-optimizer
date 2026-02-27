from __future__ import annotations

import argparse
from pathlib import Path

from vrp.data import sample_problem_data
from vrp.solver import ORToolsVRPSolver
from vrp.visualization import (
    try_write_folium_map,
    write_routes_geojson,
    write_solution_json,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Solve a capacity-constrained VRP")
    parser.add_argument("--time-limit", type=int, default=10, help="Solver time limit (sec)")
    parser.add_argument("--output-dir", type=Path, default=Path("output"))
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    problem = sample_problem_data()
    solver = ORToolsVRPSolver()
    solution = solver.solve(problem=problem, time_limit_s=args.time_limit)

    solution_path = args.output_dir / "solution.json"
    geojson_path = args.output_dir / "routes.geojson"
    map_path = args.output_dir / "routes_map.html"

    write_solution_json(solution, solution_path)
    write_routes_geojson(solution, geojson_path)
    html_written = try_write_folium_map(solution, map_path)

    print(f"Total distance (m): {solution.total_distance_m}")
    for route in solution.routes:
        stop_list = " -> ".join([stop.stop_id for stop in route.stops])
        print(
            f"{route.vehicle_id}: load={route.load}, dist={route.distance_m}m, route={stop_list}"
        )

    if solution.unassigned_customers:
        print(f"Unassigned customers: {', '.join(solution.unassigned_customers)}")
    else:
        print("All customers assigned")

    print(f"Wrote: {solution_path}")
    print(f"Wrote: {geojson_path}")
    if html_written:
        print(f"Wrote: {map_path}")
    else:
        print("Skipped HTML map (install optional dependency: pip install '.[viz]')")


if __name__ == "__main__":
    main()
