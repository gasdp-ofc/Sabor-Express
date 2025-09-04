import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from .utils import load_graph, read_deliveries, save_metrics
from .kmeans import kmeans
from .routing import route_for_cluster

def plot_graph(g, deliveries, clusters, centroids, depot, out_dir: Path):
    # Layout do grafo: usa coordenadas dos nós
    xs = [g.nodes[n][0] for n in g.nodes]
    ys = [g.nodes[n][1] for n in g.nodes]

    plt.figure()
    for u, nbrs in g.adj.items():
        ux, uy = g.nodes[u]
        for v, _ in nbrs:
            vx, vy = g.nodes[v]
            plt.plot([ux, vx], [uy, vy], linewidth=0.5)
    plt.scatter(xs, ys, s=10)
    dx, dy = g.nodes[depot]
    plt.scatter([dx], [dy], s=60, marker="s")
    plt.title("Grafo da cidade (nós e arestas)")
    out_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_dir/"graph.png", dpi=160, bbox_inches="tight")
    plt.close()

    if deliveries:
        X = np.array([g.nodes[n] for n in deliveries])
        plt.figure()
        for label in np.unique(clusters):
            pts = X[clusters == label]
            plt.scatter(pts[:,0], pts[:,1], s=25, label=f"Cluster {int(label)}")
        if centroids is not None:
            plt.scatter(centroids[:,0], centroids[:,1], s=80, marker="x")
        plt.scatter([dx], [dy], s=80, marker="s")
        plt.title("Entregas por Cluster")
        plt.legend()
        plt.savefig(out_dir/"clusters.png", dpi=160, bbox_inches="tight")
        plt.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--nodes", type=str, default="data/city_nodes.csv")
    parser.add_argument("--edges", type=str, default="data/city_edges.csv")
    parser.add_argument("--deliveries", type=str, default="data/deliveries.csv")
    parser.add_argument("--depot", type=int, default=0)
    parser.add_argument("--k", type=int, default=3, help="número de entregadores (clusters)")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", type=str, default="outputs")
    args = parser.parse_args()

    base = Path(".")
    g = load_graph(base/args.nodes, base/args.edges)
    deliveries = read_deliveries(base/args.deliveries)

    X = np.array([g.nodes[n] for n in deliveries])
    labels, centroids = kmeans(X, k=args.k, seed=args.seed)
    clusters = {i: [] for i in range(args.k)}
    for node_id, label in zip(deliveries, labels):
        clusters[int(label)].append(node_id)

    total_cost = 0.0
    cluster_costs = {}
    routes = {}

    for cid, pts in clusters.items():
        cost, path = route_for_cluster(g, pts, args.depot)
        routes[cid] = path
        cluster_costs[cid] = cost
        total_cost += cost

    avg_per_cluster = total_cost / max(args.k, 1)
    metrics = {
        "total_route_cost": total_cost,
        "cluster_costs": cluster_costs,
        "avg_cost_per_cluster": avg_per_cluster,
        "num_deliveries": len(deliveries),
        "num_clusters": args.k,
        "depot_node": args.depot,
    }

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    save_metrics(out_dir/"metrics.json", metrics)
    plot_graph(g, deliveries, labels, centroids, args.depot, out_dir)

    print("=== Sabor Express — Otimização de Rotas ===")
    print(f"Entregas: {len(deliveries)} | Entregadores (clusters): {args.k}")
    print(f"Custo total da rota: {total_cost:.2f}")
    for cid in sorted(cluster_costs.keys()):
        print(f"  Cluster {cid}: custo={cluster_costs[cid]:.2f}, paradas={len(clusters[cid])}")
    print(f"Métricas salvas em {out_dir/'metrics.json'}")
    print(f"Figuras salvas em {out_dir/'graph.png'} e {out_dir/'clusters.png'}")

if __name__ == "__main__":
    main()
