
from typing import Dict, List, Tuple
import math

class Graph:
    def __init__(self) -> None:
        self.nodes: Dict[int, Tuple[float, float]] = {}
        self.adj: Dict[int, List[Tuple[int, float]]] = {}

    def add_node(self, node_id: int, x: float, y: float) -> None:
        self.nodes[node_id] = (x, y)
        if node_id not in self.adj:
            self.adj[node_id] = []

    def add_edge(self, u: int, v: int, w: float, undirected: bool = True) -> None:
        self.adj.setdefault(u, []).append((v, w))
        if undirected:
            self.adj.setdefault(v, []).append((u, w))

    def neighbors(self, u: int) -> List[Tuple[int, float]]:
        return self.adj.get(u, [])

    def coords(self, u: int) -> Tuple[float, float]:
        return self.nodes[u]

    def euclidean(self, a: int, b: int) -> float:
        ax, ay = self.nodes[a]
        bx, by = self.nodes[b]
        return math.hypot(ax - bx, ay - by)
