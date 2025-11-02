from typing import Dict, List, Tuple

def build_grid_graph(rows: int, cols: int):
    """Return (positions, edges, neighbors) for a 4-neighbor grid graph with unit weights."""
    positions = {}
    edges = []
    neighbors = {}
    # spacing to look nice
    for r in range(rows):
        for c in range(cols):
            nid = r * cols + c
            positions[nid] = (c * 1.0, -r * 1.0)  # y inverted for top->down
            neighbors[nid] = []
    # connect 4-neighbors
    def add_edge(a, b):
        edges.append((a, b))
        neighbors[a].append(b)
        neighbors[b].append(a)

    for r in range(rows):
        for c in range(cols):
            nid = r * cols + c
            if c + 1 < cols: add_edge(nid, r * cols + (c + 1))
            if r + 1 < rows: add_edge(nid, (r + 1) * cols + c)

    return positions, edges, neighbors
