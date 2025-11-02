import time
import numpy as np
import streamlit as st

from algoviz.components.bars import make_bar_figure
from algoviz.algorithms.sorting.bubble import bubble_sort
from algoviz.algorithms.sorting.insertion import insertion_sort
from algoviz.algorithms.sorting.merge import merge_sort
from algoviz.algorithms.sorting.quick import quick_sort

st.set_page_config(page_title="Sorting Visualizer", page_icon="🔢", layout="wide")

st.title("🔢 Sorting Visualizer")
st.caption("Bubble, Insertion, Merge, and Quick Sort with playback controls + Stats HUD & Colored Regions.")

def _init_state():
    if "algo" not in st.session_state:
        st.session_state.algo = "Bubble Sort"
    if "data" not in st.session_state:
        st.session_state.data = None
    if "gen" not in st.session_state:
        st.session_state.gen = None
    if "current" not in st.session_state:
        st.session_state.current = None  # (values, highlight, swapped, meta?)
    if "playing" not in st.session_state:
        st.session_state.playing = False
    if "step" not in st.session_state:
        st.session_state.step = 0
    if "finished" not in st.session_state:
        st.session_state.finished = False
    if "cmp_count" not in st.session_state:
        st.session_state.cmp_count = 0
    if "swap_count" not in st.session_state:
        st.session_state.swap_count = 0

_init_state()

with st.sidebar:
    st.header("Controls")
    size = st.slider("Array size", min_value=10, max_value=150, value=40, step=5)
    speed_ms = st.slider("Speed (ms per step)", min_value=10, max_value=500, value=50, step=10)
    seed = st.number_input("Random seed", min_value=0, value=42, step=1)
    algo = st.selectbox("Algorithm", ["Bubble Sort", "Insertion Sort", "Merge Sort", "Quick Sort"], index=0, key="algo")

    cols = st.columns(4)
    play_pause = cols[0].button("▶/⏸", help="Play/Pause")
    step_btn   = cols[1].button("⏭ Step", help="Advance one step and pause")
    reset_btn  = cols[2].button("🔁 Reset", help="Reset to start state")
    stop_btn   = cols[3].button("⏹ Stop", help="Stop playback")

    start_btn = st.button("🎬 Start / Regenerate Data", use_container_width=True)

def _make_data(n, seed_val):
    rng = np.random.default_rng(int(seed_val))
    return rng.integers(low=1, high=100, size=n).tolist()

def _make_generator(algo_name, data):
    if algo_name == "Bubble Sort":
        return bubble_sort(data)
    elif algo_name == "Insertion Sort":
        return insertion_sort(data)
    elif algo_name == "Merge Sort":
        return merge_sort(data)
    elif algo_name == "Quick Sort":
        return quick_sort(data)
    else:
        raise ValueError("Algorithm not implemented.")

def _prime_generator():
    try:
        st.session_state.current = next(st.session_state.gen)
        st.session_state.step = 0
        st.session_state.finished = False
        st.session_state.cmp_count = 0
        st.session_state.swap_count = 0
    except StopIteration:
        st.session_state.current = None
        st.session_state.finished = True

def _update_stats_from_frame(frame):
    # frame can be 3-tuple or 4-tuple
    if frame is None:
        return
    if len(frame) >= 3:
        _, highlight, swapped = frame[0], frame[1], frame[2]
        if swapped:
            st.session_state.swap_count += 1
        elif highlight is not None:
            st.session_state.cmp_count += 1

def _advance_once():
    if st.session_state.gen is None or st.session_state.finished:
        return
    try:
        frame = next(st.session_state.gen)
        st.session_state.current = frame
        st.session_state.step += 1
        _update_stats_from_frame(frame)
    except StopIteration:
        st.session_state.finished = True
        st.session_state.playing = False

def _colors_for_frame(values, algo_name, frame):
    # Build color overrides dict {index: color}
    overrides = {}
    # Parse meta if present
    meta = {}
    if frame is not None and len(frame) >= 4 and isinstance(frame[3], dict):
        meta = frame[3]

    green = "#10b981"  # sorted regions
    blue  = "#60a5fa"  # active range
    amber = "#f59e0b"  # pivot

    n = len(values)

    if algo_name == "Bubble Sort":
        tail = meta.get("sorted_tail_len")
        if isinstance(tail, int) and tail > 0:
            start = max(0, n - tail)
            for idx in range(start, n):
                overrides[idx] = green

    if algo_name == "Insertion Sort":
        pref = meta.get("sorted_prefix_len")
        if isinstance(pref, int) and pref > 0:
            end = min(n, pref)
            for idx in range(0, end):
                overrides[idx] = green

    if algo_name in ("Merge Sort", "Quick Sort"):
        ar = meta.get("active_range")
        if isinstance(ar, tuple) and len(ar) == 2:
            lo, hi = ar
            lo = max(0, int(lo)); hi = min(n - 1, int(hi))
            for idx in range(lo, hi + 1):
                overrides[idx] = blue

    if algo_name == "Quick Sort":
        pv = meta.get("pivot")
        if isinstance(pv, int) and 0 <= pv < n:
            overrides[pv] = amber

    return overrides

# --- Button Actions ---
if start_btn:
    st.session_state.data = _make_data(size, seed)
    st.session_state.gen = _make_generator(st.session_state.algo, st.session_state.data)
    _prime_generator()
    st.session_state.playing = False
    st.toast("New data generated. Ready to play.")

if reset_btn:
    if st.session_state.data is not None:
        st.session_state.gen = _make_generator(st.session_state.algo, st.session_state.data)
        _prime_generator()
        st.session_state.playing = False
        st.toast("Reset to start.")
    else:
        st.warning("Nothing to reset. Click Start first.")

if stop_btn:
    st.session_state.playing = False

if play_pause:
    if st.session_state.current is None and st.session_state.data is None:
        st.warning("Click Start to generate data first.")
    else:
        st.session_state.playing = not st.session_state.playing

if step_btn:
    if st.session_state.current is None:
        if st.session_state.data is None:
            st.warning("Click Start to generate data first.")
        else:
            st.session_state.gen = _make_generator(st.session_state.algo, st.session_state.data)
            _prime_generator()
    else:
        _advance_once()
    st.session_state.playing = False

# --- HUD (Stats) ---
hud = st.container()
with hud:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Algorithm", st.session_state.algo)
    c2.metric("Step", st.session_state.step)
    c3.metric("Comparisons", st.session_state.cmp_count)
    c4.metric("Writes/Swaps", st.session_state.swap_count)

# --- Render ---
if st.session_state.data is None:
    preview = _make_data(size, seed)
    fig = make_bar_figure(preview, title=f"{st.session_state.algo} — Ready")
    st.plotly_chart(fig, use_container_width=True)
    st.info("Click **Start / Regenerate Data** to create a dataset and enable playback.")
else:
    if st.session_state.gen is None:
        st.session_state.gen = _make_generator(st.session_state.algo, st.session_state.data)
        _prime_generator()

    frame = st.session_state.current
    # Normalize frame to 4-tuple-like
    if frame is not None and len(frame) == 3:
        values, highlight, swapped = frame
        meta = {}
    elif frame is not None and len(frame) >= 4:
        values, highlight, swapped, meta = frame[0], frame[1], frame[2], frame[3]
    else:
        values, highlight, swapped, meta = st.session_state.data, None, False, {}

    overrides = _colors_for_frame(values, st.session_state.algo, frame)
    label = f"Step {st.session_state.step} — {'Swap' if swapped else 'Compare' if highlight is not None else '...' }"

    fig = make_bar_figure(values, highlight=highlight, title=f"{st.session_state.algo}: {label}", colors_override=overrides)
    st.plotly_chart(fig, use_container_width=True)
    st.caption(label)

    if st.session_state.playing and not st.session_state.finished:
        delay = max(10, int(speed_ms)) / 1000.0
        time.sleep(delay)
        _advance_once()
        st.rerun()

    if st.session_state.finished:
        st.success(f"Done! Sorted {len(st.session_state.data)} values in {st.session_state.step} visual steps.")
