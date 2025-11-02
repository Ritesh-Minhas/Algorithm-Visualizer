from typing import Dict, List, Tuple, Optional, Generator

Frame = Tuple[Dict, List[Tuple[int,int]], Dict[int, str], Dict[Tuple[int,int], str], Dict]

def bfs(positions, edges, neighbors, start: int, goal: Optional[int] = None) -> Generator[Frame, None, None]:
    """Breadth-first search on an unweighted graph.
    Yields frames with node_colors/edge_colors and meta (frontier size, visited count, found flag).
    """
    from collections import deque

    visited = set()
    parent = {start: None}
    q = deque([start])

    def colors(current=None, frontier=None):
        node_colors = {}
        if frontier:
            for f in frontier:
                node_colors[f] = "#60a5fa"  # blue frontier
        for v in visited:
            node_colors[v] = "#10b981"  # green visited
        if current is not None:
            node_colors[current] = "#ef4444"  # red current
        if goal is not None:
            node_colors[goal] = "#f59e0b"  # amber goal
        return node_colors, {}

    node_colors, edge_colors = colors(current=None, frontier=list(q))
    yield positions, edges, node_colors, edge_colors, {"visited": 0, "frontier": len(q), "found": False}

    while q:
        current = q.popleft()
        if current not in visited:
            visited.add(current)
            node_colors, edge_colors = colors(current, list(q))
            yield positions, edges, node_colors, edge_colors, {"visited": len(visited), "frontier": len(q), "found": current == goal}
            if current == goal:
                break
            for nxt in neighbors[current]:
                if nxt not in visited and nxt not in q:
                    parent[nxt] = current
                    q.append(nxt)
                    node_colors, edge_colors = colors(current=None, frontier=list(q))
                    yield positions, edges, node_colors, edge_colors, {"visited": len(visited), "frontier": len(q), "found": False}

    # Final highlight of shortest path if goal reached
    if goal is not None and goal in visited:
        path = []
        cur = goal
        while cur is not None:
            path.append(cur)
            cur = parent.get(cur)
        path = path[::-1]
        node_colors = {n: "#10b981" for n in visited}
        for n in path:
            node_colors[n] = "#eab308"  # yellow path
        yield positions, edges, node_colors, {}, {"visited": len(visited), "frontier": 0, "found": True, "path": path}
    else:
        node_colors = {n: "#10b981" for n in visited}
        yield positions, edges, node_colors, {}, {"visited": len(visited), "frontier": 0, "found": False}
