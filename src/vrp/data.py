from __future__ import annotations

import math

from vrp.models import Customer, Depot, Location, ProblemData, Vehicle


def haversine_distance_m(a: Location, b: Location) -> int:
    radius_m = 6_371_000
    lat1 = math.radians(a.lat)
    lon1 = math.radians(a.lon)
    lat2 = math.radians(b.lat)
    lon2 = math.radians(b.lon)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    h = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    return int(2 * radius_m * math.asin(math.sqrt(h)))


def build_distance_matrix(depot: Depot, customers: list[Customer]) -> list[list[int]]:
    points = [depot.location] + [c.location for c in customers]
    size = len(points)
    matrix: list[list[int]] = [[0] * size for _ in range(size)]

    for i in range(size):
        for j in range(size):
            if i != j:
                matrix[i][j] = haversine_distance_m(points[i], points[j])
    return matrix


def sample_problem_data() -> ProblemData:
    # Example around Austin, TX.
    depot = Depot(id="DEPOT-ATX", location=Location(lat=30.2672, lon=-97.7431))
    customers = [
        Customer("C001", Location(30.2799, -97.7360), demand=2),
        Customer("C002", Location(30.2500, -97.7500), demand=3),
        Customer("C003", Location(30.2950, -97.7200), demand=4),
        Customer("C004", Location(30.2400, -97.7000), demand=2),
        Customer("C005", Location(30.3100, -97.7400), demand=5),
        Customer("C006", Location(30.2200, -97.7600), demand=2),
        Customer("C007", Location(30.2600, -97.6800), demand=3),
        Customer("C008", Location(30.2850, -97.7800), demand=4),
        Customer("C009", Location(30.3300, -97.7100), demand=1),
        Customer("C010", Location(30.2100, -97.7300), demand=2),
    ]
    vehicles = [
        Vehicle("TRUCK-1", capacity=10),
        Vehicle("TRUCK-2", capacity=10),
        Vehicle("TRUCK-3", capacity=10),
    ]

    distance_matrix = build_distance_matrix(depot, customers)
    return ProblemData(
        depot=depot,
        customers=customers,
        vehicles=vehicles,
        distance_matrix=distance_matrix,
    )
