import streamlit as st

st.set_page_config(page_title="Algorithm Visualizer", page_icon="🧠", layout="wide")
st.title("🧠 Algorithm Visualizer (Python + Streamlit)")
st.write(
    "Welcome! This project makes classic algorithms **visual and intuitive**. "
    "Use the sidebar to open the **Sorting** page, where you can play Bubble, Insertion, Merge, and Quick sort with full playback controls."
)
st.markdown("---")
st.subheader("How this works (high level)")
st.write(
    "- Each algorithm is a **generator** that yields the array state step-by-step.\n"
    "- The UI consumes those states to animate via Plotly.\n"
    "- The codebase is **modular**: add algorithms without touching much UI."
)
st.info("Open the **Sorting** page from the left sidebar to try it out.")
