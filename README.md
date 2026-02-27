# Route Optimizer (VRP)

A production-style starter for solving Vehicle Routing Problems (VRP) with OR-Tools.

## What it solves

- Minimize total delivery distance
- Respect per-vehicle capacity constraints
- Assign customers to trucks
- Produce route artifacts you can visualize
- Keep architecture extensible for future real-time optimization

## Project structure

- `src/vrp/models.py`: domain entities and solution schema
- `src/vrp/data.py`: sample realistic data + distance matrix generation
- `src/vrp/solver.py`: OR-Tools VRP solver
- `src/vrp/visualization.py`: GeoJSON + optional HTML map export
- `src/vrp/main.py`: CLI entrypoint

## Quickstart

1. Create environment and install:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

2. Run solver:

```bash
python -m vrp.main --output-dir output --time-limit 10
```

3. Outputs:

- `output/solution.json`: structured solution summary
- `output/routes.geojson`: route geometries for GIS/web maps
- `output/routes_map.html`: optional interactive map (if `folium` is installed)

## Real-time extensibility notes

- Distance provider can be replaced with external routing APIs.
- `ProblemData` is serializable and can be streamed/updated incrementally.
- Solver config is isolated so objectives/constraints can be expanded.
