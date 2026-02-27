from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(slots=True)
class Location:
    lat: float
    lon: float


@dataclass(slots=True)
class Depot:
    id: str
    location: Location


@dataclass(slots=True)
class Customer:
    id: str
    location: Location
    demand: int


@dataclass(slots=True)
class Vehicle:
    id: str
    capacity: int


@dataclass(slots=True)
class ProblemData:
    depot: Depot
    customers: list[Customer]
    vehicles: list[Vehicle]
    # Distances in meters. Matrix index: 0=depot, 1..N=customers.
    distance_matrix: list[list[int]]


@dataclass(slots=True)
class RouteStop:
    node_index: int
    stop_id: str
    lat: float
    lon: float
    cumulative_load: int


@dataclass(slots=True)
class VehicleRoute:
    vehicle_id: str
    stops: list[RouteStop]
    distance_m: int
    load: int


@dataclass(slots=True)
class VRPSolution:
    routes: list[VehicleRoute]
    total_distance_m: int
    unassigned_customers: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
