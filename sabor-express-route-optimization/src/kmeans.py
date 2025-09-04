
from typing import Tuple
import numpy as np

def kmeans(X: np.ndarray, k: int, max_iter: int = 100, seed: int = 42) -> Tuple[np.ndarray, np.ndarray]:
    """
    Simple K-Means.
    Returns (labels, centroids).
    """
    rng = np.random.default_rng(seed)
    n, d = X.shape
    # init by choosing k random points
    indices = rng.choice(n, size=k, replace=False)
    centroids = X[indices].copy()

    labels = np.zeros(n, dtype=int)

    for _ in range(max_iter):
        # assign
        dists = np.linalg.norm(X[:, None, :] - centroids[None, :, :], axis=2)  # (n, k)
        new_labels = dists.argmin(axis=1)

        if np.array_equal(new_labels, labels):
            break
        labels = new_labels

        # update
        for i in range(k):
            pts = X[labels == i]
            if len(pts) > 0:
                centroids[i] = pts.mean(axis=0)
            else:
                # reinitialize empty cluster to random point
                centroids[i] = X[rng.integers(0, n)]
    return labels, centroids
