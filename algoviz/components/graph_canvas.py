from typing import Dict, List, Tuple, Optional, Set
import plotly.graph_objects as go

# Types
# positions: Dict[int, Tuple[float,float]]
# edges: List[Tuple[int,int]]

def make_graph_figure(positions: Dict[int, Tuple[float,float]],
                      edges: List[Tuple[int,int]],
                      title: str = "",
                      node_colors: Optional[Dict[int, str]] = None,
                      edge_colors: Optional[Dict[Tuple[int,int], str]] = None) -> go.Figure:
    """Create a clean Plotly figure for an undirected graph."""
    node_x = []
    node_y = []
    node_ids = []
    for nid, (x, y) in positions.items():
        node_x.append(x)
        node_y.append(y)
        node_ids.append(nid)

    base_node_color = "#94a3b8"  # grey
    colors = [node_colors.get(n, base_node_color) if node_colors else base_node_color for n in node_ids]

    # Edge traces
    edge_x = []
    edge_y = []
    edge_line_colors = []
    for (u, v) in edges:
        x0, y0 = positions[u]
        x1, y1 = positions[v]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
        if edge_colors and (u, v) in edge_colors:
            edge_line_colors.append(edge_colors[(u, v)])
        elif edge_colors and (v, u) in edge_colors:
            edge_line_colors.append(edge_colors[(v, u)])
        else:
            edge_line_colors.append("#475569")  # slate-600

    fig = go.Figure()

    # Draw edges as a single scattergl trace for performance
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y,
                               mode="lines",
                               line=dict(width=2),
                               hoverinfo="none",
                               showlegend=False))

    # Draw nodes
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode="markers+text",
        text=[str(n) for n in node_ids],
        textposition="top center",
        marker=dict(size=16, color=colors, line=dict(width=2, color="#0f1115")),
        hoverinfo="text",
        showlegend=False
    ))

    fig.update_layout(
        title=title,
        margin=dict(l=10, r=10, t=45, b=10),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor="#0f1115",
        paper_bgcolor="#0f1115",
    )
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    return fig
