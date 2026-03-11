import streamlit as st
import pandas as pd
import sqlite3
import os

# 1. Page Configuration
st.set_page_config(page_title="Neal Kauffman | Data Portfolio", page_icon="📊", layout="wide")

# --- CUSTOM CSS FOR HIGH-VISIBILITY TABS ---
st.markdown("""
    <style>
    /* Make the tab text much larger and bold */
    button[data-baseweb="tab"] {
        font-size: 24px !important;
        font-weight: bold !important;
        color: #555;
    }
    /* Highlight the active tab with a distinct color */
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #ff4b4b !important;
    }
    /* Make the underline thicker */
    div[data-baseweb="tab-highlight"] {
        background-color: #ff4b4b !important;
        height: 4px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE FOR SCOREBOARD ---
if 'step' not in st.session_state:
    st.session_state.step = 1 
if 'num_teams' not in st.session_state:
    st.session_state.num_teams = 2
if 'teams' not in st.session_state:
    st.session_state.teams = []
if 'feedback_msg' not in st.session_state:
    st.session_state.feedback_msg = "READY TO PLAY"

# --- 2. DYNAMIC NAVIGATION SIDEBAR ---
st.sidebar.title("Navigation")

category = st.sidebar.selectbox("Choose a Section:", 
    ["Main", "Games/Apps", "Case Studies", "Resources"]
)

if category == "Main":
    page = st.sidebar.radio("Go to:", ["Home", "About Me"])
elif category == "Games/Apps":
    page = st.sidebar.radio("Go to:", ["Trivia Scoreboard", "Alien Invasion Game"])
elif category == "Case Studies":
    page = st.sidebar.radio("Go to:", ["IMDB Insights"])
elif category == "Resources":
    page = st.sidebar.radio("Go to:", ["Reference Guide"])

# --- PAGE LOGIC ---

if page == "Home":
    st.title("Welcome to My Data Portfolio")
    st.markdown("""
    ### Hello! I'm Neal Kauffman. **Computer Systems** student at Collin College transitioning into Data Analytics.
    This portfolio is a live demonstration of my skills in **Data Analysis, SQL Transformation, Data Visualization and Python Development.**
    
    Use the navigation menu on the left to explore:
    - **IMDB Insights:** A full ETL pipeline from Excel to SQL and Power BI.
    - **Interactive Apps:** Custom-built Python tools like the Trivia Scoreboard.
    - **Game Dev:** Logic and structure for a Python-based space shooter.
    """)
    st.info("Select a project from the sidebar to get started!")

elif page == "About Me":
    st.title("About Me")
    st.markdown("""
    I am a Data Analyst specializing in building robust data pipelines and interactive visualizations. 
    My background in the restaurant industry taught me the importance of efficiency and clear communication—traits I now apply to data architecture.
    
    **Technical Toolbox:**
    - **Languages:** SQL (T-SQL, SQLite), Python
    - **Tools:** Excel (Power Query, VBA), Power BI, Streamlit, Git
    - **Education:** Computer Systems / Data Analytics at Collin College
    """)

elif page == "Trivia Scoreboard":
    st.title("🏆 Interactive Trivia Scoreboard")
    
    if st.session_state.step == 1:
        st.subheader("Step 1: Setup Teams")
        num = st.number_input("How many teams are playing?", min_value=2, max_value=10, value=st.session_state.num_teams)
        if st.button("Initialize Teams"):
            st.session_state.num_teams = num
            st.session_state.teams = [{"name": f"Team {i+1}", "score": 0} for i in range(num)]
            st.session_state.step = 2
            st.rerun()

    elif st.session_state.step == 2:
        st.subheader("Step 2: Live Scoring")
        cols = st.columns(len(st.session_state.teams))
        for i, team in enumerate(st.session_state.teams):
            with cols[i]:
                st.metric(team['name'], team['score'])
                if st.button(f"Steal (+1) {team['name']}", key=f"plus_{i}"):
                    st.session_state.teams[i]['score'] += 1
                    st.rerun()
                if st.button(f"Adjust (-1) {team['name']}", key=f"minus_{i}"):
                    st.session_state.teams[i]['score'] -= 1
                    st.rerun()
        
        st.divider()
        if st.button("Reset Game"):
            st.session_state.step = 1
            st.rerun()

elif page == "Alien Invasion Game":
    st.title("👾 Alien Invasion: Python Game Development")
    st.markdown("""
    ### Project Overview
    This project is a 2D space shooter built entirely in Python using the **Pygame** library. 
    It demonstrates core software engineering principles, including **Object-Oriented Programming (OOP)**, 
    asynchronous event handling, and real-time asset management.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Key Features")
        st.write("""
        - **Dynamic Difficulty:** Alien fleet speed increases as the player progresses.
        - **Asset Management:** Custom sprite handling for ships, bullets, and enemies.
        - **Scoring System:** High-score persistence across game sessions.
        """)
        
    with col2:
        st.subheader("Technical Stack")
        st.code("""
import pygame
import sys
from settings import Settings
from ship import Ship
        """, language='python')

elif page == "IMDB Insights":
    st.title("🎬 Case Study: IMDB Data Warehouse")
    
    # --- BIG TABS ---
    tab_sql, tab_excel = st.tabs(["SQL Cleaning Scripts & Queries", "Excel Data Prep"])

    with tab_sql:
        st.subheader("🔍 SQL Portfolio Showcase")
        st.write("Select a script below to see the T-SQL logic I wrote, followed by a live preview:")
        
        query_selection = st.selectbox("Select Script:", [
            "1. ETL: Dynamic Data Cleaning (Votes)",
            "2. Analysis: The Decade Trend",
            "3. Analysis: Genre Dominance",
            "4. ETL: The Final Power BI View"
        ])

        # --- AUTO-BUILD THE DATABASE ---
        if not os.path.exists('imdb.db'):
            try:
                raw_df = pd.read_csv('IMBD_Final_CSV.csv')
                raw_df.columns = raw_df.columns.str.strip()
                if 'title' in raw_df.columns:
                    raw_df = raw_df.drop(columns=['title'])
                setup_conn = sqlite3.connect('imdb.db')
                raw_df.to_sql('movies', setup_conn, if_exists='replace', index=False)
                setup_conn.close()
            except FileNotFoundError:
                st.error("Missing 'IMBD_Final_CSV.csv'. Please upload it to GitHub!")
                st.stop() 

        try:
            conn = sqlite3.connect('imdb.db')
            
            if query_selection == "1. ETL: Dynamic Data Cleaning (Votes)":
                st.markdown("**Objective:** Convert a dirty string column containing 'M' (millions) and 'K' (thousands) into a usable numeric format.")
                st.code('''
UPDATE Movies
SET Votes_Clean = CASE 
    WHEN Votes LIKE '%M' THEN TRY_CAST(REPLACE(Votes, 'M', '') AS DECIMAL(10,2)) * 1000000
    WHEN Votes LIKE '%K' THEN TRY_CAST(REPLACE(Votes, 'K', '') AS DECIMAL(10,2)) * 1000
    ELSE TRY_CAST(REPLACE(Votes, ',', '') AS DECIMAL(10,2))
END;
                ''', language='sql')
                query = 'SELECT Title, "Start Year", Votes, "Popularity Tier" FROM movies LIMIT 15'
                df = pd.read_sql_query(query, conn)
                st.dataframe(df, use_container_width=True)

            elif query_selection == "2. Analysis: The Decade Trend":
                st.markdown("**Objective:** Group movies by decade to analyze rating trends.")
                st.code('''
SELECT 
    FLOOR(Start_Year / 10) * 10 AS Decade,
    COUNT(*) AS Total_Movies,
    CAST(AVG(Rating) AS DECIMAL(10,2)) AS Avg_Rating
FROM Movies
WHERE Start_Year IS NOT NULL
GROUP BY FLOOR(Start_Year / 10) * 10
ORDER BY Decade DESC;
                ''', language='sql')
                query = 'SELECT Decade, COUNT(*) AS Total_Movies, ROUND(AVG(Rating), 2) AS Avg_Rating FROM movies WHERE Decade IS NOT NULL GROUP BY Decade ORDER BY Decade DESC'
                df = pd.read_sql_query(query, conn)
                col1, col2 = st.columns([1, 2])
                with col1: st.dataframe(df, use_container_width=True)
                with col2: st.line_chart(data=df.set_index('Decade')['Avg_Rating'])

            elif query_selection == "3. Analysis: Genre Dominance":
                st.markdown("**Objective:** Identify which genres produce the most content and calculate quality.")
                st.code('''
SELECT TOP 10
    Genre,
    COUNT(*) AS Movie_Count,
    CAST(AVG(Rating) AS DECIMAL(10,2)) AS Genre_Avg_Rating
FROM Movies
GROUP BY Genre
ORDER BY Movie_Count DESC;
                ''', language='sql')
                query = "SELECT Genre, COUNT(*) AS Movie_Count, ROUND(AVG(Rating), 2) AS Genre_Avg_Rating FROM movies WHERE Genre IS NOT NULL GROUP BY Genre ORDER BY Movie_Count DESC LIMIT 10"
                df = pd.read_sql_query(query, conn)
                col1, col2 = st.columns([1, 2])
                with col1: st.dataframe(df, use_container_width=True)
                with col2: st.bar_chart(data=df.set_index('Genre')['Movie_Count'])

            elif query_selection == "4. ETL: The Final Power BI View":
                st.markdown("**Objective:** Final standardized View for Power BI ingestion.")
                st.code('''
CREATE OR ALTER VIEW v_Master_Movies AS
SELECT
    Title,
    Start_Year,
    FLOOR(Start_Year / 10) * 10 AS Decade,
    CAST(Rating AS DECIMAL(10,2)) AS Rating,
    Votes_Clean AS Votes, 
    TRIM(Genre) AS Genre,
    CASE
        WHEN Votes_Clean >= 10000 THEN 'High Popularity'
        WHEN Votes_Clean >= 1000 THEN 'Medium Popularity'
        ELSE 'Low Popularity'
    END AS Popularity_Category,
    Stars
FROM Movies;
                ''', language='sql')
                df = pd.read_sql_query("SELECT * FROM movies LIMIT 100", conn)
                st.dataframe(df, use_container_width=True)

            st.divider()
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Cleaned CSV Result", data=csv_data, file_name='Neal_Kauffman_IMDB_Cleaned.csv', mime='text/csv')
            conn.close()
        except Exception as e:
            st.error(f"Error loading data: {e}")

    with tab_excel:
        st.subheader("📊 Part 1: Excel Data Prep")
        st.markdown("""
        Before the data reached the SQL Warehouse, I utilized Microsoft Excel to perform initial auditing and sanity checks.
        
        **Cleaning Logic Applied:**
        - **Data Auditing:** Used Pivot Tables to identify inconsistent naming and rating outliers.
        - **Formatting:** Normalized the `Start Year` column and stripped hidden whitespace.
        - **VLOOKUP:** Cross-referenced title lists to ensure data integrity across exports.
        """)
        try:
            with open("IMBD_Cleaned_Final.xlsm", "rb") as file:
                st.download_button(
                    label="📂 Download Cleaned Excel Workbook (.xlsm)",
                    data=file,
                    file_name="Neal_Kauffman_IMDB_Prep.xlsm",
                    mime="application/vnd.ms-excel.sheet.macroEnabled.12"
                )
        except FileNotFoundError:
            st.warning("Excel file 'IMBD_Cleaned_Final.xlsm' not found in the repository.")

elif page == "Reference Guide":
    st.title("📚 Reference Guide")
    st.markdown("""
    As part of my continuous learning and workflow optimization, I built and maintain a standalone 
    **Data Analyst Reference Guide**. It serves as a live documentation tool for Python syntax, 
    SQL queries, and data visualization techniques.
    """)
    
    st.info("Click below to open the live reference app in a new, full-screen tab.")
    
    # A professional button to open the app in a new tab
    st.link_button("Launch Full Reference Guide App ↗️", "https://analyst-reference-guide-ntkauffman1.streamlit.app/", type="primary", use_container_width=True)
