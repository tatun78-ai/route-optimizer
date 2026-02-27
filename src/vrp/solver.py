from __future__ import annotations

from ortools.constraint_solver import pywrapcp, routing_enums_pb2

from vrp.models import ProblemData, RouteStop, VRPSolution, VehicleRoute


class ORToolsVRPSolver:
    def solve(self, problem: ProblemData, time_limit_s: int = 10) -> VRPSolution:
        manager = pywrapcp.RoutingIndexManager(
            len(problem.distance_matrix),
            len(problem.vehicles),
            0,
        )
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index: int, to_index: int) -> int:
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return problem.distance_matrix[from_node][to_node]

        transit_idx = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_idx)

        demands = [0] + [c.demand for c in problem.customers]

        def demand_callback(from_index: int) -> int:
            from_node = manager.IndexToNode(from_index)
            return demands[from_node]

        demand_idx = routing.RegisterUnaryTransitCallback(demand_callback)
        capacities = [v.capacity for v in problem.vehicles]
        routing.AddDimensionWithVehicleCapacity(
            demand_idx,
            0,
            capacities,
            True,
            "Capacity",
        )

        for node in range(1, len(problem.distance_matrix)):
            routing.AddDisjunction([manager.NodeToIndex(node)], 100_000)

        search = pywrapcp.DefaultRoutingSearchParameters()
        search.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )
        search.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        )
        search.time_limit.seconds = time_limit_s

        solution = routing.SolveWithParameters(search)
        if solution is None:
            raise RuntimeError("No feasible VRP solution found")

        routes: list[VehicleRoute] = []
        total_distance = 0
        visited_customers: set[str] = set()

        for v_idx, vehicle in enumerate(problem.vehicles):
            index = routing.Start(v_idx)
            route_distance = 0
            route_load = 0
            stops: list[RouteStop] = []

            while not routing.IsEnd(index):
                node_index = manager.IndexToNode(index)
                if node_index == 0:
                    stop_id = problem.depot.id
                    lat = problem.depot.location.lat
                    lon = problem.depot.location.lon
                else:
                    cust = problem.customers[node_index - 1]
                    stop_id = cust.id
                    lat = cust.location.lat
                    lon = cust.location.lon
                    route_load += cust.demand
                    visited_customers.add(cust.id)

                stops.append(
                    RouteStop(
                        node_index=node_index,
                        stop_id=stop_id,
                        lat=lat,
                        lon=lon,
                        cumulative_load=route_load,
                    )
                )

                next_index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(index, next_index, v_idx)
                index = next_index

            stops.append(
                RouteStop(
                    node_index=0,
                    stop_id=problem.depot.id,
                    lat=problem.depot.location.lat,
                    lon=problem.depot.location.lon,
                    cumulative_load=route_load,
                )
            )

            routes.append(
                VehicleRoute(
                    vehicle_id=vehicle.id,
                    stops=stops,
                    distance_m=route_distance,
                    load=route_load,
                )
            )
            total_distance += route_distance

        unassigned = [c.id for c in problem.customers if c.id not in visited_customers]

        return VRPSolution(
            routes=routes,
            total_distance_m=total_distance,
            unassigned_customers=unassigned,
        )
