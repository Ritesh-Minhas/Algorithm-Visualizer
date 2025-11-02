from typing import Dict, List, Tuple, Optional, Generator

Frame = Tuple[Dict, List[Tuple[int,int]], Dict[int, str], Dict[Tuple[int,int], str], Dict]

def dfs(positions, edges, neighbors, start: int, goal: Optional[int] = None) -> Generator[Frame, None, None]:
    """Depth-first search (iterative). Yields frames with node_colors and meta."""
    stack = [start]
    visited = set()
    parent = {start: None}

    def colors(current=None, stack_snap=None):
        node_colors = {}
        if stack_snap:
            for s in stack_snap:
                node_colors[s] = "#60a5fa"  # blue stack nodes
        for v in visited:
            node_colors[v] = "#10b981"  # green visited
        if current is not None:
            node_colors[current] = "#ef4444"  # red current
        if goal is not None:
            node_colors[goal] = "#f59e0b"  # amber goal
        return node_colors, {}

    node_colors, edge_colors = colors(current=None, stack_snap=list(stack))
    yield positions, edges, node_colors, edge_colors, {"visited": 0, "stack": len(stack), "found": False}

    while stack:
        current = stack.pop()
        if current not in visited:
            visited.add(current)
            node_colors, edge_colors = colors(current, list(stack))
            yield positions, edges, node_colors, edge_colors, {"visited": len(visited), "stack": len(stack), "found": current == goal}
            if current == goal:
                break
            # push neighbors (reverse to get visually consistent order)
            for nxt in reversed(neighbors[current]):
                if nxt not in visited and nxt not in stack:
                    parent[nxt] = current
                    stack.append(nxt)
                    node_colors, edge_colors = colors(current=None, stack_snap=list(stack))
                    yield positions, edges, node_colors, edge_colors, {"visited": len(visited), "stack": len(stack), "found": False}

    # Final (optional path highlight if goal reached)
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
        yield positions, edges, node_colors, {}, {"visited": len(visited), "stack": 0, "found": True, "path": path}
    else:
        node_colors = {n: "#10b981" for n in visited}
        yield positions, edges, node_colors, {}, {"visited": len(visited), "stack": 0, "found": False}
