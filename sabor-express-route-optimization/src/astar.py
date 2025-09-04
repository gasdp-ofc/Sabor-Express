
import heapq
from typing import Dict, Tuple, List, Optional
from .graph import Graph

def astar(graph: Graph, start: int, goal: int) -> Tuple[float, List[int]]:
    """Return (cost, path) from start to goal using A*."""
    open_heap: List[Tuple[float, int]] = []
    heapq.heappush(open_heap, (0.0, start))

    g_score: Dict[int, float] = {start: 0.0}
    came_from: Dict[int, Optional[int]] = {start: None}

    while open_heap:
        _, current = heapq.heappop(open_heap)
        if current == goal:
            # reconstruct
            path = [current]
            while came_from[current] is not None:
                current = came_from[current]  # type: ignore
                path.append(current)
            path.reverse()
            return g_score[path[-1]], path

        for neighbor, weight in graph.neighbors(current):
            tentative = g_score[current] + weight
            if tentative < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative
                f = tentative + graph.euclidean(neighbor, goal)  # h(n)
                heapq.heappush(open_heap, (f, neighbor))

    return float('inf'), []  # no path
