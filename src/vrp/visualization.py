from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from vrp.models import VRPSolution


def solution_to_geojson(solution: VRPSolution) -> dict[str, Any]:
    features: list[dict[str, Any]] = []
    for route in solution.routes:
        coords = [[s.lon, s.lat] for s in route.stops]
        features.append(
            {
                "type": "Feature",
                "properties": {
                    "vehicle_id": route.vehicle_id,
                    "distance_m": route.distance_m,
                    "load": route.load,
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": coords,
                },
            }
        )

    return {
        "type": "FeatureCollection",
        "features": features,
    }


def write_solution_json(solution: VRPSolution, out_path: Path) -> None:
    out_path.write_text(json.dumps(solution.to_dict(), indent=2), encoding="utf-8")


def write_routes_geojson(solution: VRPSolution, out_path: Path) -> None:
    geo = solution_to_geojson(solution)
    out_path.write_text(json.dumps(geo, indent=2), encoding="utf-8")


def try_write_folium_map(solution: VRPSolution, out_path: Path) -> bool:
    try:
        import folium
    except ImportError:
        return False

    first_stop = solution.routes[0].stops[0]
    fmap = folium.Map(location=[first_stop.lat, first_stop.lon], zoom_start=11)

    palette = ["red", "blue", "green", "orange", "cadetblue", "darkred"]
    for idx, route in enumerate(solution.routes):
        color = palette[idx % len(palette)]
        points = [(s.lat, s.lon) for s in route.stops]
        folium.PolyLine(
            points,
            color=color,
            weight=4,
            opacity=0.8,
            tooltip=f"{route.vehicle_id}: {route.distance_m}m",
        ).add_to(fmap)

        for stop in route.stops:
            folium.CircleMarker(
                location=[stop.lat, stop.lon],
                radius=4,
                popup=f"{stop.stop_id} | load={stop.cumulative_load}",
                color=color,
                fill=True,
            ).add_to(fmap)

    fmap.save(str(out_path))
    return True
