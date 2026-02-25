import streamlit as st

st.set_page_config(page_title="Neal's Data Portfolio", page_icon="📊")

st.title("🚀 Neal Kauffman | Data Analytics Portfolio")
st.write("Current Student at Collin College | Contract Web Analyst")

# --- PROJECT 1: SCOREBOARD ---
st.header("1. Interactive Game Scoreboard")
if 'score' not in st.session_state:
    st.session_state.score = 0

col1, col2, col3 = st.columns([1,1,2])
with col1:
    if st.button('Steal (+1)'): st.session_state.score += 1
with col2:
    if st.button('Adjust (-1)'): st.session_state.score -= 1
with col3:
    st.subheader(f"Current Score: {st.session_state.score}")

# --- PROJECT 2: IMDB DATA WAREHOUSE (Placeholder) ---
st.divider()
st.header("2. IMDB Data Warehouse")
st.write("Coming soon: SQL-driven analysis of movie trends.")
