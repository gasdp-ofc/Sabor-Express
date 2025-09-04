
from typing import List, Tuple, Dict
import math
from .graph import Graph
from .astar import astar

def nearest_neighbor_order(graph: Graph, waypoints: List[int], start: int) -> List[int]:
    """Greedy order of visiting waypoints using straight-line distance from current node."""
    remaining = set(waypoints)
    order: List[int] = []
    current = start
    while remaining:
        nxt = min(remaining, key=lambda w: graph.euclidean(current, w))
        order.append(nxt)
        remaining.remove(nxt)
        current = nxt
    return order

def route_for_cluster(graph: Graph, cluster_points: List[int], depot: int) -> Tuple[float, List[int]]:
    """Build full route (sequence of node ids) starting at depot, visiting all cluster points, and returning to depot.
       Uses A* between consecutive stops and greedy ordering."""
    if not cluster_points:
        return 0.0, [depot]

    order = nearest_neighbor_order(graph, cluster_points, depot)

    total_cost = 0.0
    full_path: List[int] = [depot]

    current = depot
    for stop in order:
        cost, path = astar(graph, current, stop)
        if not path:
            return math.inf, []
        total_cost += cost
        # append without duplicating current
        full_path += path[1:]
        current = stop

    # return to depot
    cost, path = astar(graph, current, depot)
    if not path:
        return math.inf, []
    total_cost += cost
    full_path += path[1:]

    return total_cost, full_path
