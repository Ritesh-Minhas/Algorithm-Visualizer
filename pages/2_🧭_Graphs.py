import time
import streamlit as st

from algoviz.components.graph_canvas import make_graph_figure
from algoviz.algorithms.graphs.utils import build_grid_graph
from algoviz.algorithms.graphs.bfs import bfs
from algoviz.algorithms.graphs.dfs import dfs
from algoviz.algorithms.graphs.dijkstra import dijkstra

st.set_page_config(page_title="Graph Algorithms", page_icon="🧭", layout="wide")

st.title("🧭 Graph Algorithms")
st.caption("BFS, DFS, and Dijkstra on a grid graph with playback controls and a stats HUD.")

def _init_state():
    if "g_algo" not in st.session_state:
        st.session_state.g_algo = "BFS"
    if "g_positions" not in st.session_state:
        st.session_state.g_positions = None
    if "g_edges" not in st.session_state:
        st.session_state.g_edges = None
    if "g_neighbors" not in st.session_state:
        st.session_state.g_neighbors = None
    if "g_gen" not in st.session_state:
        st.session_state.g_gen = None
    if "g_current" not in st.session_state:
        st.session_state.g_current = None  # (positions, edges, node_colors, edge_colors, meta)
    if "g_playing" not in st.session_state:
        st.session_state.g_playing = False
    if "g_step" not in st.session_state:
        st.session_state.g_step = 0
    if "g_finished" not in st.session_state:
        st.session_state.g_finished = False

_init_state()

with st.sidebar:
    st.header("Graph Controls")
    cols_rc = st.columns(2)
    rows = cols_rc[0].number_input("Rows", min_value=3, max_value=20, value=6, step=1)
    cols = cols_rc[1].number_input("Cols", min_value=3, max_value=30, value=8, step=1)

    g_algo = st.selectbox("Algorithm", ["BFS", "DFS", "Dijkstra"], index=0, key="g_algo")

    # Start & goal nodes by index (row-major id = r*cols + c)
    start = st.number_input("Start node id", min_value=0, max_value=rows*cols-1, value=0, step=1)
    goal = st.number_input("Goal node id", min_value=0, max_value=rows*cols-1, value=rows*cols-1, step=1)

    cols_btn = st.columns(4)
    play_pause = cols_btn[0].button("▶/⏸", help="Play/Pause")
    step_btn   = cols_btn[1].button("⏭ Step", help="Advance one step and pause")
    reset_btn  = cols_btn[2].button("🔁 Reset", help="Reset to start state")
    stop_btn   = cols_btn[3].button("⏹ Stop", help="Stop playback")

    start_btn = st.button("🎬 Build Graph & Start", use_container_width=True)

def _make_generator(name, positions, edges, neighbors, s, g):
    if name == "BFS":
        return bfs(positions, edges, neighbors, s, g)
    if name == "DFS":
        return dfs(positions, edges, neighbors, s, g)
    if name == "Dijkstra":
        return dijkstra(positions, edges, neighbors, s, g)
    raise ValueError("Unknown algorithm.")

def _prime_generator():
    try:
        st.session_state.g_current = next(st.session_state.g_gen)
        st.session_state.g_step = 0
        st.session_state.g_finished = False
    except StopIteration:
        st.session_state.g_current = None
        st.session_state.g_finished = True

def _advance_once():
    if st.session_state.g_gen is None or st.session_state.g_finished:
        return
    try:
        st.session_state.g_current = next(st.session_state.g_gen)
        st.session_state.g_step += 1
    except StopIteration:
        st.session_state.g_finished = True
        st.session_state.g_playing = False

if start_btn:
    pos, edg, nbr = build_grid_graph(int(rows), int(cols))
    st.session_state.g_positions = pos
    st.session_state.g_edges = edg
    st.session_state.g_neighbors = nbr

    st.session_state.g_gen = _make_generator(st.session_state.g_algo, pos, edg, nbr, int(start), int(goal))
    _prime_generator()
    st.session_state.g_playing = False
    st.toast("Graph built. Ready to play.")

if reset_btn:
    if st.session_state.g_positions is not None:
        st.session_state.g_gen = _make_generator(st.session_state.g_algo, st.session_state.g_positions, st.session_state.g_edges, st.session_state.g_neighbors, int(start), int(goal))
        _prime_generator()
        st.session_state.g_playing = False
        st.toast("Reset to start.")
    else:
        st.warning("Nothing to reset. Click Build Graph & Start first.")

if stop_btn:
    st.session_state.g_playing = False

if play_pause:
    if st.session_state.g_current is None and st.session_state.g_positions is None:
        st.warning("Click Build Graph & Start first.")
    else:
        st.session_state.g_playing = not st.session_state.g_playing

if step_btn:
    if st.session_state.g_current is None:
        if st.session_state.g_positions is None:
            st.warning("Click Build Graph & Start first.")
        else:
            st.session_state.g_gen = _make_generator(st.session_state.g_algo, st.session_state.g_positions, st.session_state.g_edges, st.session_state.g_neighbors, int(start), int(goal))
            _prime_generator()
    else:
        _advance_once()
    st.session_state.g_playing = False

# HUD
hud = st.container()
with hud:
    c1, c2, c3 = st.columns(3)
    c1.metric("Algorithm", st.session_state.g_algo)
    c2.metric("Step", st.session_state.g_step)
    # show a third metric based on algorithm
    if st.session_state.g_current and len(st.session_state.g_current) >= 5:
        meta = st.session_state.g_current[4]
        if st.session_state.g_algo == "BFS":
            c3.metric("Visited / Frontier", f"{meta.get('visited', 0)} / {meta.get('frontier', 0)}")
        elif st.session_state.g_algo == "DFS":
            c3.metric("Visited / Stack", f"{meta.get('visited', 0)} / {meta.get('stack', 0)}")
        else:
            c3.metric("Visited / Queue", f"{meta.get('visited', 0)} / {meta.get('queue', 0)}")
    else:
        c3.metric("Status", "Idle")

# Render
if st.session_state.g_positions is None:
    st.info("Set **Rows/Cols**, choose an **algorithm**, then click **Build Graph & Start**.")
else:
    if st.session_state.g_current is None:
        fig = make_graph_figure(st.session_state.g_positions, st.session_state.g_edges, title=f"{st.session_state.g_algo} — Ready")
        st.plotly_chart(fig, use_container_width=True)
    else:
        positions, edges, node_colors, edge_colors, meta = st.session_state.g_current
        title = f"{st.session_state.g_algo}: Step {st.session_state.g_step}"                + (" — FOUND!" if meta.get("found") else "")
        fig = make_graph_figure(positions, edges, title=title, node_colors=node_colors, edge_colors=edge_colors)
        st.plotly_chart(fig, use_container_width=True)

    if st.session_state.g_playing and not st.session_state.g_finished:
        # speed shares the slider from Sorting page scope, so give it a default
        delay_ms = 80
        time.sleep(delay_ms / 1000.0)
        _advance_once()
        st.rerun()

    if st.session_state.g_finished and st.session_state.g_current is not None:
        meta = st.session_state.g_current[4] if len(st.session_state.g_current) >= 5 else {}
        if meta.get("found"):
            st.success("Target reached! Path highlighted in yellow.")
        else:
            st.info("Traversal complete.")
