from typing import Iterable, Optional, Tuple, Dict
import plotly.graph_objects as go

def make_bar_figure(values: Iterable[int],
                    highlight: Optional[Tuple[int, ...]] = None,
                    title: str = "",
                    colors_override: Optional[Dict[int, str]] = None) -> go.Figure:
    """Create a Plotly bar chart.
    - highlight: indices to emphasize (red)
    - colors_override: dict {index: hex_color} for custom regions (e.g., sorted prefix/suffix, pivot)
    """
    x = list(range(len(values)))
    base_color = "#94a3b8"  # slate-400
    hi_color = "#ef4444"    # red-500

    colors = [base_color for _ in x]

    # Apply custom color overrides first
    if colors_override:
        for idx, col in colors_override.items():
            if 0 <= idx < len(colors):
                colors[idx] = col

    # Then apply highlight (takes precedence)
    if highlight is not None:
        for idx in highlight:
            if 0 <= idx < len(colors):
                colors[idx] = hi_color

    fig = go.Figure(
        data=[
            go.Bar(
                x=x,
                y=values,
                marker=dict(color=colors),
                hoverinfo="x+y",
            )
        ]
    )

    fig.update_layout(
        title=title,
        margin=dict(l=10, r=10, t=45, b=10),
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        height=420,
    )
    return fig
