from typing import Dict, List, Tuple, Optional, Generator
import heapq

Frame = Tuple[Dict, List[Tuple[int,int]], Dict[int, str], Dict[Tuple[int,int], str], Dict]

def dijkstra(positions, edges, neighbors, start: int, goal: Optional[int] = None, weights=None) -> Generator[Frame, None, None]:
    """Dijkstra with unit weights by default. Yields frames with node colors and meta distances."""
    nodelist = list(positions.keys())
    dist = {n: float("inf") for n in nodelist}
    dist[start] = 0.0
    parent = {start: None}
    visited = set()
    pq = [(0.0, start)]

    def colors(current=None, pq_nodes=None):
        node_colors = {}
        if pq_nodes:
            for s in pq_nodes:
                node_colors[s] = "#60a5fa"  # blue in-queue
        for v in visited:
            node_colors[v] = "#10b981"  # green settled
        if current is not None:
            node_colors[current] = "#ef4444"  # red current
        if goal is not None:
            node_colors[goal] = "#f59e0b"  # amber goal
        return node_colors, {}

    node_colors, edge_colors = colors(None, [start])
    yield positions, edges, node_colors, edge_colors, {"visited": 0, "queue": 1, "dist": dict(dist), "found": False}

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        node_colors, edge_colors = colors(u, [v for _, v in pq])
        yield positions, edges, node_colors, edge_colors, {"visited": len(visited), "queue": len(pq), "dist": dict(dist), "found": u == goal}
        if u == goal:
            break
        for v in neighbors[u]:
            w = 1.0 if weights is None else weights.get((u, v), weights.get((v, u), 1.0))
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heapq.heappush(pq, (nd, v))
                node_colors, edge_colors = colors(None, [x for _, x in pq])
                yield positions, edges, node_colors, edge_colors, {"visited": len(visited), "queue": len(pq), "dist": dict(dist), "found": False}

    # Final path highlight
    if goal is not None and goal in parent:
        path = []
        cur = goal
        while cur is not None:
            path.append(cur)
            cur = parent.get(cur)
        path = path[::-1]
        node_colors = {n: "#10b981" for n in visited}
        for n in path:
            node_colors[n] = "#eab308"  # yellow path
        yield positions, edges, node_colors, {}, {"visited": len(visited), "queue": 0, "dist": dict(dist), "found": True, "path": path}
    else:
        node_colors = {n: "#10b981" for n in visited}
        yield positions, edges, node_colors, {}, {"visited": len(visited), "queue": 0, "dist": dict(dist), "found": False}
