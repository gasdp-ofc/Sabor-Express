
from typing import Dict, List, Tuple
import csv
import json
from pathlib import Path

def load_graph(nodes_csv: Path, edges_csv: Path):
    from .graph import Graph
    g = Graph()
    with open(nodes_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            g.add_node(int(row["id"]), float(row["x"]), float(row["y"]))
    with open(edges_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            g.add_edge(int(row["u"]), int(row["v"]), float(row["w"]), undirected=True)
    return g

def read_deliveries(deliveries_csv: Path) -> List[int]:
    ids: List[int] = []
    with open(deliveries_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ids.append(int(row["node_id"]))
    return ids

def save_metrics(path: Path, metrics: Dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
