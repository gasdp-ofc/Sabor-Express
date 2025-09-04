from typing import Dict, List, Tuple
import math

class Graph:
    def __init__(self) -> None:
        # dicionário de nós: id -> (x, y)
        self.nodes: Dict[int, Tuple[float, float]] = {}
        # lista de adjacência: u -> [(v, peso)]
        self.adj: Dict[int, List[Tuple[int, float]]] = {}

    def add_node(self, node_id: int, x: float, y: float) -> None:
        self.nodes[node_id] = (x, y)
        if node_id not in self.adj:
            self.adj[node_id] = []

    def add_edge(self, u: int, v: int, w: float, undirected: bool = True) -> None:
        # adiciona aresta u -> v com peso w; se 'undirected', também v -> u
        self.adj.setdefault(u, []).append((v, w))
        if undirected:
            self.adj.setdefault(v, []).append((u, w))

    def neighbors(self, u: int) -> List[Tuple[int, float]]:
        # retorna vizinhos de u com seus pesos
        return self.adj.get(u, [])

    def coords(self, u: int) -> Tuple[float, float]:
        # retorna coordenadas (x, y) do nó u
        return self.nodes[u]

    def euclidean(self, a: int, b: int) -> float:
        # distância euclidiana entre nós a e b
        ax, ay = self.nodes[a]
        bx, by = self.nodes[b]
        return math.hypot(ax - bx, ay - by)
