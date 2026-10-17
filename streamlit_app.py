import streamlit as st
import pandas as pd
import sqlite3
import os
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(page_title="Neal Kauffman | Professional Portfolio", page_icon="📊", layout="wide")

# --- CUSTOM CSS FOR HIGH-VISIBILITY TABS & HOME CARDS ---
st.markdown("""
    <style>
    /* Make the tab text much larger and bold (Adjusted to 18px to fit 5 tabs) */
    button[data-baseweb="tab"] {
        font-size: 18px !important;
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
    /* Card layout for Home Directory */
    .nav-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 16px;
        margin-top: 20px;
        margin-bottom: 25px;
    }
    .nav-card {
        background-color: var(--secondary-background-color, #1e2530);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 12px;
        padding: 20px;
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .nav-card:hover {
        transform: translateY(-4px);
        border-color: #ff4b4b;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.25);
    }
    .nav-card-title {
        font-size: 1.15rem;
        font-weight: 700;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
        color: var(--text-color, #ffffff);
    }
    .nav-card-desc {
        font-size: 0.9rem;
        color: rgba(200, 200, 200, 0.85);
        line-height: 1.45;
        margin: 0;
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

# Flipped the order of Case Studies and Games/Apps
category = st.sidebar.selectbox("Choose a Section:", 
    ["Main", "Case Studies", "Games/Apps", "Resources", "Site Architecture"]
)

if category == "Main":
    page = st.sidebar.radio("Go to:", ["Home", "About Me"])
elif category == "Case Studies":
    page = st.sidebar.radio("Go to:", [
        "IMDB Insights", 
        "ITPM Prioritization Business Case", 
        "Systems Analysis & Architecture", 
        "More Coming Soon!"
    ])
elif category == "Games/Apps":
    page = st.sidebar.radio("Go to:", ["Trivia Scoreboard", "Alien Invasion Game"])
elif category == "Resources":
    page = st.sidebar.radio("Go to:", ["Reference Guide"])
elif category == "Site Architecture":
    page = st.sidebar.radio("Go to:", ["System Health", "Tech Stack"])

# --- SYSTEM HEALTH TEASER (DYNAMIC VERSION) ---
st.sidebar.markdown("---")

# Default values
uptime_display = "99.9%"
status_icon = "🟢"

# Calculate Live Uptime from CSV
file_path = "app_performance_log.csv"
if os.path.exists(file_path):
    try:
        stats_df = pd.read_csv(file_path, names=["Timestamp", "App", "Load Time (s)", "Status"])
        if not stats_df.empty:
            total_pings = len(stats_df)
            successes = len(stats_df[stats_df["Status"] == "Success"])
            uptime_pct = (successes / total_pings) * 100
            uptime_display = f"{uptime_pct:.1f}%"
            
            # Change icon to yellow if uptime drops below 95%
            if uptime_pct < 95:
                status_icon = "🟡"
    except:
        pass

st.sidebar.markdown(f"{status_icon} **System Status:** All apps online")
st.sidebar.caption(f"CI/CD Pipeline: Active | Uptime: {uptime_display}")

if page == "Home":
    st.title("Welcome to My Professional Portfolio")
    st.markdown("""
    ### Hello! I’m Neal Kauffman, a Technology Management student at East Texas A&M University and a graduate of Collin College, where I earned an Associate of Applied Science in Computer Information Systems.

This portfolio began as a showcase for my data analytics work and is growing into a broader collection of projects across information technology, systems, data, and technology management.

Currently hosted: data analytics projects, SQL work, Python development, and data visualization.

Coming soon: systems administration, IT project management, Windows and Linux labs, networking, scripting, and IBM Z/mainframe-related work.
    """)
    
    st.markdown("""
    <p style="font-size: 1.05rem; opacity: 0.9;">
        Use the navigation menu on the left to explore:
    </p>

    <div class="nav-container">
        <div class="nav-card">
            <div class="nav-card-title">🎬 IMDB Insights</div>
            <p class="nav-card-desc">Full ETL pipeline extracting raw records into SQL and Power BI dashboards.</p>
        </div>
        <div class="nav-card">
            <div class="nav-card-title">📋 ITPM Business Case</div>
            <p class="nav-card-desc">Executive project prioritization matrix, financial ROI models, and cost-reduction analysis.</p>
        </div>
        <div class="nav-card">
            <div class="nav-card-title">🏗️ Systems Analysis & Arch</div>
            <p class="nav-card-desc">End-to-end SDLC order system case study: DFDs, UML models, 3NF SQL schema, and 3-tier AWS architecture.</p>
        </div>
        <div class="nav-card">
            <div class="nav-card-title">🛠️ Interactive Apps</div>
            <p class="nav-card-desc">Custom-built Python tools, game logic, and dynamic state engines like the Trivia Scoreboard.</p>
        </div>
        <div class="nav-card">
            <div class="nav-card-title">👾 Game Dev</div>
            <p class="nav-card-desc">Object-oriented architecture, collision logic, and loop engines for a Python space shooter.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("Select a project from the sidebar to get started!")

elif page == "About Me":
    st.title("About Me")
    
    # 1. ADD YOUR PHOTO HERE
    photo_filename = "495352114_10162816845657138_4891462490022732075_n.jpg"
    
    try:
        st.image(photo_filename, caption="Neal Kauffman", width=250)
    except FileNotFoundError:
        st.error(f"Image not found. Please place '{photo_filename}' in your VS Code folder.")
    st.markdown("""
    I am currently an Online Data Researcher with a strong foundation in Python and SQL. 
    
    Before pursuing my degree in Computer Systems and transitioning into data analytics, I spent several years managing fast-paced environments in the restaurant industry as a Front of House Manager and Bartender. 
    
    This background gave me a unique perspective on customer experience, daily operations, and the critical importance of making accurate, data-driven business decisions to improve efficiency.
                
                **Technical Toolbox:**
    - **Languages:** SQL (T-SQL, SQLite), Python
    - **Tools:** Excel (Power Query, VBA), Power BI, Streamlit, Git, AI
    - **Education:** Computer Information Systems at Collin College - Completion Summer 2026
    - **Certs:** Google Data Analytics Professional Certificate         
    """)

elif page == "System Health":
    st.title("⚙️ System Health (CI/CD)")
    st.subheader("Automated Performance Tracking")
    st.markdown("""
    As an analyst, I believe in tracking everything—including my own portfolio. 
    This live dashboard reads from a CSV generated daily by a custom **GitHub Actions CI/CD pipeline** that I built. It uses **Selenium** to test my apps, ensuring zero cold-starts and logging the server response times.
    """)
    
    # Point this to your new CSV file
    file_path = "app_performance_log.csv"
    
    if os.path.exists(file_path):
        try:
            # Load the data
            df = pd.read_csv(file_path, names=["Timestamp", "App", "Load Time (s)", "Status"])
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            
            # Filter for successful loads to chart
            success_df = df[df["Status"] == "Success"]
            
            if not success_df.empty:
                # Pivot data for the multi-line chart
                chart_data = success_df.pivot(index="Timestamp", columns="App", values="Load Time (s)")
                
                st.line_chart(
                    chart_data, 
                    x_label="Time of Ping", 
                    y_label="Server Load Time (Seconds)")
                                            
                
                with st.expander("View Raw Automated ETL Logs"):
                    st.dataframe(df.sort_values(by="Timestamp", ascending=False), use_container_width=True)
            else:
                st.info("Pipeline is live. Waiting for first successful data points...")
                
        except Exception as e:
            st.warning(f"Could not load performance logs. ({e})")
    else:
        st.info("Performance pipeline initialized. Data will appear after the next automated run.")
        st.divider()
        
elif page == "Tech Stack":
    st.title("🛠️ Tech Stack & Architecture Rationale")
    st.markdown("""
    A data project is only as reliable as the infrastructure it runs on. 
    Here is a breakdown of the tools I selected to build, deploy, and maintain this portfolio.
    """)

    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **Frontend & Hosting:** Streamlit Community Cloud
        
        Chosen for its ability to rapidly deploy Python-based data applications. It allows me to bridge the gap between complex data logic and a clean user interface without the overhead of maintaining a separate React or JavaScript frontend.
        """)
        
        st.success("""
        **Database Engine:** SQLite
        
        Selected for the IMDB Case Study to provide lightweight, embedded SQL querying. By compiling the database locally at runtime, I avoid the latency, API bottlenecks, and costs associated with a dedicated cloud database for static portfolio data.
        """)
        
    with col2:
        st.warning("""
        **Automation & CI/CD:** GitHub Actions + Selenium
        
        Used to engineer a custom ETL testing pipeline. To prevent the free-tier server from hibernating, a headless Chrome browser spins up twice a day on an Ubuntu virtual machine, verifies the UI renders correctly, and commits the performance logs back to the repository.
        """)
        
        st.error("""
        **Data Processing:** Pandas 
        
        The core engine for my data manipulation. Utilized heavily across the portfolio for fast CSV parsing, programmatic data transformation, and feeding clean, structured data into the Streamlit visualization layers.
        """)

elif page == "Trivia Scoreboard":
    st.title("🏆 Interactive Trivia Scoreboard")
     # --- STEP 1: TEAM COUNT SCREEN ---
    if st.session_state.step == 1:
        st.title("🏅 Game Setup")
        st.session_state.num_teams = st.number_input(
            "How many teams? (Max 6)", min_value=1, max_value=6, value=2, step=1
        )
        if st.button("Next: Set Up Teams ➡️", use_container_width=True):
            st.session_state.step = 2
            st.rerun()

    # --- STEP 2: TEAM NAMES & COLORS SCREEN ---
    elif st.session_state.step == 2:
        st.title("🎨 Team Setup")
        colors = ["Red", "Blue", "Green", "Yellow", "Purple", "Orange"]
        temp_teams = []
        
        for i in range(st.session_state.num_teams):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input(f"Team {i+1} Name", value=f"Team {i+1}", key=f"name_{i}")
            with col2:
                color = st.selectbox(f"Team {i+1} Color", options=colors, key=f"color_{i}")
            
            temp_teams.append({"name": name, "color": color, "score": 0.0})
            
        st.divider()
        if st.button("🚀 Start Game!", use_container_width=True, type="primary"):
            st.session_state.teams = temp_teams
            st.session_state.step = 3
            st.rerun()

    # --- STEP 3: MAIN SCOREBOARD SCREEN ---
    elif st.session_state.step == 3:
        st.title("🎯 Live Scoreboard")
        st.info(f"**{st.session_state.feedback_msg}**")
        st.divider()
        
        hex_map = {
            "Red": "#b31f1f", "Blue": "#439af1", "Green": "#06c235",
            "Yellow": "#eec10c", "Purple": "#593DAC", "Orange": "#ee7c0a"
        }

        max_score = max([t["score"] for t in st.session_state.teams]) if st.session_state.teams else 0
        cols = st.columns(len(st.session_state.teams))
        
        for i, col in enumerate(cols):
            team = st.session_state.teams[i]
            with col:
                leader_marker = "👑 " if team["score"] == max_score and max_score > 0 else ""
                team_hex = hex_map.get(team['color'], "#ffffff")
                st.markdown(f"""
                    <div style='background-color: {team_hex}; padding: 15px; border-radius: 10px; text-align: center; border: 2px solid #333; margin-bottom: 15px;'>
                        <h2 style='margin: 0; color: black;'>{leader_marker}{team['name']}</h2>
                    </div>
                """, unsafe_allow_html=True)
                
                score_display = int(team["score"]) if team["score"].is_integer() else team["score"]
                st.metric(label="Score", value=score_display)
                
                if st.button("Song Name (+1)", key=f"song_{i}", use_container_width=True):
                    st.session_state.teams[i]["score"] += 1
                    st.session_state.feedback_msg = f"★ {team['name']} scored Song Name! ★"
                    st.rerun()
                if st.button("Artist (+1)", key=f"art_{i}", use_container_width=True):
                    st.session_state.teams[i]["score"] += 1
                    st.session_state.feedback_msg = f"★ {team['name']} scored Artist! ★"
                    st.rerun()
                if st.button("Extra (+1)", key=f"ext_{i}", use_container_width=True):
                    st.session_state.teams[i]["score"] += 1
                    st.session_state.feedback_msg = f"★ {team['name']} scored Extra! ★"
                    st.rerun()
                    
                st.markdown("---") 
                
                if st.button("Partial (+0.5)", key=f"part_{i}", use_container_width=True):
                    st.session_state.teams[i]["score"] += 0.5
                    st.session_state.feedback_msg = f"★ {team['name']} scored Partial! ★"
                    st.rerun()
                    
                if st.button("Bonus (+3)", key=f"bon_{i}", type="primary", use_container_width=True):
                    st.session_state.teams[i]["score"] += 3
                    st.session_state.feedback_msg = f"🔥 {team['name']} scored a BONUS! 🔥"
                    st.balloons() 
                    st.rerun()
                    
                if st.button("Steal (+1)", key=f"steal_{i}", use_container_width=True):
                    st.session_state.teams[i]["score"] += 1
                    st.session_state.feedback_msg = f"🥷 {team['name']} stole a point! 🥷"
                    st.rerun()
                if st.button("Adjust (-1)", key=f"adj_{i}", use_container_width=True):
                    st.session_state.teams[i]["score"] -= 1
                    st.session_state.feedback_msg = f"Adjusted {team['name']}'s score."
                    st.rerun()

        st.divider()
        col_reset, col_exit = st.columns(2)
        with col_reset:
            if st.button("⚠️ Reset Scores", use_container_width=True):
                for t in st.session_state.teams:
                    t["score"] = 0.0
                st.session_state.feedback_msg = "SCORES RESET"
                st.rerun()
        with col_exit:
            if st.button("❌ End Game (Start Over)", use_container_width=True):
                st.session_state.step = 1
                st.session_state.teams = []
                st.session_state.feedback_msg = "READY TO PLAY"
                st.rerun()

elif page == "Alien Invasion Game":
    st.title("👾 Alien Invasion: Python Game Development")
    
    st.markdown("""
    ### Project Overview
    This project is a classic 2D space arcade shooter built entirely in Python using the **Pygame** library. 
    It demonstrates core software engineering principles, including **Object-Oriented Programming (OOP)**, 
    asynchronous event handling, and real-time asset management, all compiled to WebAssembly for the browser.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Key Features")
        st.write("""
        - **Dynamic Difficulty:** Alien fleet speed increases as the player progresses.
        - **Asset Management:** Custom sprite handling for ships, bullets, and enemies.
        - **Scoring System:** High-score tracking and arcade-style auto-restarts.
        """)
        
    with col2:
        st.subheader("Technical Stack")
        st.code("""
import pygame
import sys
from settings import Settings
from ship import Ship
        """, language='python')

    # Add a visual divider before the playable game section
    st.divider()

    st.header("🎮 Play the Game")
    st.info("Click the black screen below to focus the game, then use your **Spacebar** to shoot and **Left/Right Arrow Keys** to move!")

    game_url = "https://ntkauffman1.github.io/alien-invasion-game/"

    components.iframe(game_url, width=1200, height=850, scrolling=False)

elif page == "IMDB Insights":
    st.title("🎬 Case Study: IMDB Data Warehouse")
    
    # --- 5 BIG TABS ---
    tab_sql, tab_excel, tab_pbi, tab_python, tab_html = st.tabs([
        "SQL Cleaning Scripts & Queries", 
        "Excel Data Prep",
        "Power BI Dashboard", 
        "Python Correlation Analysis", 
        "Project Findings Page"
    ])

    with tab_sql:
        st.subheader("🔍 SQL Portfolio Showcase")
        
        # --- NEW ADDITION: Download SQL file ---
        try:
            with open("IMDB_Project_Queries_Revised.sql", "rb") as sql_file:
                st.download_button(
                    label="📂 Download Full T-SQL Script (.sql)",
                    data=sql_file,
                    file_name="IMDB_Project_Queries_Revised.sql",
                    mime="application/sql"
                )
        except FileNotFoundError:
            st.warning("SQL file 'IMDB_Project_Queries_Revised.sql' not found in the repository.")
        
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
        
        **Cleaning Logic and Steps Applied:**
        - **Data Auditing:** Used Pivot Tables to identify inconsistent naming and rating outliers.
        - **Formatting:** Normalized the `Start Year` column and stripped hidden whitespace.
        - **VLOOKUP:** Cross-referenced title lists to ensure data integrity across exports.
        - **Macro:** Update Dashboard Macro added to Pivot Tab.
        - **Documentation:** Steps, Formulas, and Logic documented in Deliverables Tab.
        """)
        
        # --- NEW ADDITION: Raw Data Download ---
        try:
            with open("IMDB_Raw_Data.csv", "rb") as raw_file:
                st.download_button(
                    label="📄 Download Raw Data (.csv)",
                    data=raw_file,
                    file_name="IMDB_Raw_Data.csv",
                    mime="text/csv"
                )
        except FileNotFoundError:
            st.warning("Raw Data file 'IMDB_Raw_Data.csv' not found in the repository.")
            
        try:
            with open("IMBD_Cleaned_Final.xlsm", "rb") as file:
                st.download_button(
                    label="📂 Download Cleaned Excel Workbook (.xlsm)",
                    data=file,
                    file_name="IMDB_Cleaned_Final.xlsm",
                    mime="application/vnd.ms-excel.sheet.macroEnabled.12"
                )
        except FileNotFoundError:
            st.warning("Excel file 'IMBD_Cleaned_Final.xlsm' not found in the repository.")

    # =========================================================================
    # TAB 3: POWER BI
    # =========================================================================
    with tab_pbi:
        st.subheader("📈 Executive Power BI Dashboard")
        st.markdown("""
        I connected Power BI directly to the cleaned SQL Data Warehouse to build an interactive dashboard tracking genre performance and rating trends over time. 
        This acts as the final reporting layer for business stakeholders.
        """)
        
        try:
            st.image("dashboard.png", caption="IMDB Analytics Interactive Dashboard", use_container_width=True)
        except FileNotFoundError:
            st.warning("Upload 'dashboard.png' to GitHub to see the image preview here.")
            
        col1, col2 = st.columns(2)
        with col1:
            try:
                with open("IMDB_Analytics_Dashboard.pbix", "rb") as file:
                    st.download_button("📊 Download Interactive .pbix File", data=file, file_name="IMDB_Analytics_Dashboard.pbix", mime="application/octet-stream")
            except FileNotFoundError: pass
        with col2:
            try:
                with open("IMDB_Analytics_Dashboard.pdf", "rb") as file:
                    st.download_button("📄 Download Dashboard as PDF", data=file, file_name="IMDB_Analytics_Dashboard.pdf", mime="application/pdf")
            except FileNotFoundError: pass

    # =========================================================================
    # TAB 4: PYTHON ANALYSIS
    # =========================================================================
    with tab_python:
        st.subheader("🐍 Python Statistical Analysis")
        st.markdown("""
        Using `pandas`, `seaborn`, and `pyodbc`, I connected directly to the SQL Server to analyze statistical correlations. 
        Specifically, I wanted to answer: *Does the popularity of a movie (Votes) correlate with higher Ratings?*
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            try:
                st.image("heatmap.png", caption="Correlation Heatmap Matrix", use_container_width=True)
            except FileNotFoundError: pass
        with col2:
            try:
                st.image("scatter_plot.png", caption="Votes vs. Rating Scatter Plot", use_container_width=True)
            except FileNotFoundError: pass
            
        st.markdown("### Raw Python Script (`movie_analysis.py`)")
        try:
            with open("movie_analysis.py", "r", encoding="utf-8") as f:
                st.code(f.read(), language='python')
                
            with open("movie_analysis.py", "rb") as f:
                st.download_button("⬇️ Download Python Script", data=f, file_name="movie_analysis.py", mime="text/x-python-script")
        except FileNotFoundError:
            st.warning("Upload 'movie_analysis.py' to GitHub to view the code.")

    # =========================================================================
    # TAB 5: HTML SUMMARY
    # =========================================================================
    with tab_html:
        st.subheader("🌐 HTML Project Findings Page")
        st.markdown("""
        To present these findings to non-technical stakeholders, I built a lightweight HTML/CSS landing page. 
        This demonstrates my ability to communicate data insights effectively across web formats.
        """)
        
        try:
            with open("index.html", "r", encoding="utf-8") as f:
                html_data = f.read()
                
                # 1. This renders the actual live webpage inside your app!
                import streamlit.components.v1 as components
                components.html(html_data, height=600, scrolling=True)
                
                # 2. This puts the raw code inside a dropdown menu so it doesn't clutter the screen
                with st.expander("🔍 View Raw HTML Code"):
                    st.code(html_data, language='html')
                
            with open("index.html", "rb") as f:
                st.download_button("⬇️ Download Raw index.html", data=f, file_name="index.html", mime="text/html")
        except FileNotFoundError:
            st.warning("Upload 'index.html' to GitHub to view the project.")

elif page == "ITPM Prioritization Business Case":
    st.title("📋 IT Project Evaluation & Prioritization")
    st.subheader("Manage Your Health, INC — Executive Business Case[cite: 1]")

    st.markdown("""
    > **Context:** Executive assessment evaluating four competing IT initiatives to reduce operational costs, modernize infrastructure, and recover capital from an estimated 20% excess in healthcare premiums across 20,000 full-time employees[cite: 1].
    """)

    # Executive Summary Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="Top Priority Initiative",
            value="Wellness Intranet",
            help="Recommended based on fast payback period and immediate cost reduction[cite: 1]."
        )
    with col2:
        st.metric(
            label="Projected Annual Savings",
            value="$600,000",
            delta="Immediate Cost Reduction[cite: 1]"
        )
    with col3:
        st.metric(
            label="Estimated Initial Cost",
            value="$200,000"
        )
    with col4:
        st.metric(
            label="Payback Period",
            value="< 6 Months",
            delta="Rapid ROI[cite: 1]"
        )

    st.markdown("---")

    st.subheader("📊 Strategic Evaluation Matrix")

    portfolio_data = [
        {
            "Project Name": "Recreation and Wellness Intranet",
            "Strategic Focus": "Internal Cost Reduction",
            "Upfront Cost": 200000,
            "Net Annual Benefit": 600000,
            "4-Year Net Value": 2200000,
            "Strategic Impact": "High",
            "Key Non-Financial Benefit": "Employee health, retention, and morale"
        },
        {
            "Project Name": "Health Coverage Business Model",
            "Strategic Focus": "Cost Reduction & App Dev",
            "Upfront Cost": 100000,
            "Net Annual Benefit": 400000,
            "4-Year Net Value": 1500000,
            "Strategic Impact": "High",
            "Key Non-Financial Benefit": "Data-driven leverage for premium negotiations"
        },
        {
            "Project Name": "Cross-Selling System",
            "Strategic Focus": "Revenue Growth",
            "Upfront Cost": 800000,
            "Net Annual Benefit": 200000,
            "4-Year Net Value": 0,
            "Strategic Impact": "Medium",
            "Key Non-Financial Benefit": "Customer retention via targeted discounting"
        },
        {
            "Project Name": "Web-Enhanced Comms System",
            "Strategic Focus": "Web Ops & Delivery Optimization",
            "Upfront Cost": 3000000,
            "Net Annual Benefit": 1400000,
            "4-Year Net Value": 2600000,
            "Strategic Impact": "High (Deferred)",
            "Key Non-Financial Benefit": "Streamlined supply chain logistics"
        }
    ]

    df_itpm = pd.DataFrame(portfolio_data)

    st.dataframe(
        df_itpm,
        column_config={
            "Upfront Cost": st.column_config.NumberColumn(format="$%d"),
            "Net Annual Benefit": st.column_config.NumberColumn(format="$%d/yr"),
            "4-Year Net Value": st.column_config.NumberColumn(format="$%d"),
        },
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    st.subheader("🔍 Financial Back-Up & Projections")

    tab_itpm1, tab_itpm2, tab_itpm3, tab_itpm4 = st.tabs([
        "1. Recreation & Wellness Intranet",
        "2. Health Coverage Model",
        "3. Cross-Selling System",
        "4. Web-Enhanced Comms"
    ])

    with tab_itpm1:
        st.markdown("""
        * **Employee Base:** 20,000 full-time employees[cite: 1]
        * **Per-Employee Savings:** $30 / employee / year[cite: 1]
        * **Gross Annual Savings:** **$600,000 / year**[cite: 1]
        * **4-Year Cumulative Savings:** **$2,400,000**[cite: 1]
        * **Implementation Cost:** $200,000[cite: 1]
        * **Verdict:** **Immediate Priority.** Fully recovers upfront implementation costs within 4 to 5 months of rollout (well before the 6-month deadline)[cite: 1].
        """)

    with tab_itpm2:
        st.markdown("""
        * **Employee Base:** 20,000 full-time employees[cite: 1]
        * **Per-Employee Savings:** $20 / employee / year[cite: 1]
        * **Gross Annual Savings:** **$400,000 / year**[cite: 1]
        * **4-Year Cumulative Savings:** **$1,600,000**[cite: 1]
        * **Implementation Cost:** $100,000[cite: 1]
        * **Verdict:** High ROI secondary candidate[cite: 1]. Combining this with the Wellness Intranet yields **$1,000,000/yr in recurring operational savings** against an initial combined $300,000 investment[cite: 1].
        """)

    with tab_itpm3:
        st.markdown("""
        * **Gross Annual Revenue:** $1,000,000[cite: 1]
        * **Recurring Maintenance / Dev Cost:** $800,000 / year[cite: 1]
        * **Net Annual Profit:** **$200,000 / year**[cite: 1]
        * **Verdict:** **Requires Re-evaluation.** High maintenance overhead cuts margins down to 20%[cite: 1]. Recommend negotiating vendor/development costs before committing capital[cite: 1].
        """)

    with tab_itpm4:
        st.markdown("""
        * **Initial Investment:** $3,000,000 (Year 1)[cite: 1]
        * **Gross Annual Operational Savings:** $2,000,000 / year[cite: 1]
        * **Annual Maintenance (20%):** $600,000 / year[cite: 1]
        * **Net Annual Benefit:** **$1,400,000 / year** (starting Year 2)[cite: 1]
        * **Verdict:** Offers the largest absolute long-term savings, but demands significant upfront capital[cite: 1]. Recommended as a phase-two initiative after short-term savings are secured[cite: 1].
        """)

    with st.expander("📌 View Recommendation & Phased Implementation Memo"):
        st.markdown("""
        ### Final Recommendation Memo
        1. **Phase 1 (Immediate Execution):** Greenlight the **Recreation and Wellness Intranet Project** ($200k cost) and **Health Coverage Business Model** ($100k cost)[cite: 1]. Combined, they yield ~$1,000,000 in immediate recurring annual savings on a modest $300,000 total outlay[cite: 1].
        2. **Phase 2 (Long-term Infrastructure):** Sequence the **Web-Enhanced Communications System** once early Phase 1 cash flows normalize, offsetting the $3.0M upfront capital requirement[cite: 1].
        3. **Phase 3 (Scope Reassessment):** Pause the **Cross-Selling System** until maintenance and development overhead can be engineered down to a sustainable operating ratio[cite: 1].
        """)

elif page == "Systems Analysis & Architecture":
    st.title("🏗️ Systems Analysis & Cloud Architecture")
    st.subheader("Mackinac Gnomes Order Management System (OMS)[cite: 20]")
    st.caption("Authored by Neal Kauffman | Comprehensive Systems Analysis & SDLC Deliverable[cite: 20]")

    st.markdown("""
    > **Executive Summary:** A complete, phased systems analysis transitioning Mackinac Gnomes from a single, error-prone spreadsheet to a secure, cloud-native transactional web portal[cite: 20]. This case study covers stakeholder elicitation, process modeling (DFDs & UML), third-normal-form (3NF) relational design, and a multi-tier AWS VPC architecture[cite: 20].
    """)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="System Baseline", value="2.6 / 5.0", delta="Legacy User Rating", delta_color="inverse")
    with col2:
        st.metric(label="Usage Velocity", value="75%", delta="Accesses ≥ 6x Daily")
    with col3:
        st.metric(label="Automation Priority", value="50 / 50 Split", help="50% automated shipping labels vs 50% automated sales calculation[cite: 20]")
    with col4:
        st.metric(label="Security Posture", value="3-Tier VPC", delta="Subnet Defense in Depth[cite: 20]")

    st.markdown("---")

    tab_slides, tab_sa1, tab_sa2, tab_sa3, tab_sa4, tab_sa5, tab_sa6 = st.tabs([
        "📑 Slide Presentation",
        "📊 Requirements & Surveys",
        "🔄 Data Flow Diagrams (DFDs)",
        "📐 UML & Logic Models",
        "🗄️ Relational Schema (3NF)",
        "☁️ Cloud Architecture & Memo",
        "📅 WBS & Implementation Plan"
    ])

    # ----------------- TAB: SLIDE PRESENTATION VIEWER -----------------
    with tab_slides:
        st.header("📑 Executive Systems Analysis Deck")
        st.markdown("Scroll through the complete slide presentation below, or download the PDF directly.")

        pdf_path = "Mackinac Gnomes Order Management System pdf.pdf"

        if os.path.exists(pdf_path):
            import base64

            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()
                base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

            # Action controls
            c_dl1, c_dl2 = st.columns([1, 3])
            with c_dl1:
                st.download_button(
                    label="⬇️ Download Presentation (.pdf)",
                    data=pdf_bytes,
                    file_name="Mackinac_Gnomes_Systems_Analysis.pdf",
                    mime="application/pdf"
                )

            # Native browser scrollable PDF embed
            pdf_display = f'''
                <iframe
                    src="data:application/pdf;base64,{base64_pdf}"
                    width="100%"
                    height="850"
                    type="application/pdf"
                    style="border-radius: 8px; border: 1px solid rgba(128, 128, 128, 0.3);">
                </iframe>
            '''
            st.markdown(pdf_display, unsafe_allow_html=True)
        else:
            st.warning("Presentation file 'Mackinac Gnomes Order Management System pdf.pdf' not found in repo root.")
            st.link_button(
                "📂 View Presentation on GitHub ↗️",
                "https://github.com/ntkauffman1/professional-portfolio/blob/main/Mackinac%20Gnomes%20Order%20Management%20System%20pdf.pdf"
            )

    with tab_sa1:
        st.header("1. Stakeholder Requirements Gathering & Feedback Analysis")
        st.markdown("""
        Requirements were gathered from key organizational roles (**Sales**, **Accounting**, and **Creation/Production**) to identify root-cause inefficiencies in the existing order tracking spreadsheet[cite: 20].
        """)

        col_q1, col_q2 = st.columns(2)
        with col_q1:
            st.subheader("Spreadsheet Daily Usage Frequency")
            df_usage = pd.DataFrame({
                "Access Frequency": ["1–5 times / day", "6–15 times / day", "15+ times / day (Heavy users)"],
                "Respondents": ["25%", "25%", "50%"]
            })
            st.dataframe(df_usage, hide_index=True, use_container_width=True)
            st.warning("⚠️ **Core Bottleneck:** 75% of users accessed the spreadsheet 6+ times a day, leading to concurrency collisions and overwrites[cite: 20].")

        with col_q2:
            st.subheader("Primary Automation Driver")
            df_auto = pd.DataFrame({
                "Automated Capability Requested": [
                    "Auto-generating shipping labels/tickets",
                    "Auto-calculating weekly sales",
                    "Alerting production when sale finalized",
                    "Sending confirmation emails to customers"
                ],
                "Preference": ["50%", "50%", "0%", "0%"]
            })
            st.dataframe(df_auto, hide_index=True, use_container_width=True)
            st.info("💡 **Finding:** User demand was evenly divided between logistics (shipping ticket creation) and finance (automated weekly reporting)[cite: 20].")

        with st.expander("🔍 View Peer Review & Iterative Survey Enhancements"):
            st.markdown("""
            #### Peer Review Cycle & Survey Refinements
            * **Xavier Infante:** Validated the necessity of **Refund and Replacement Status fields** to trace damaged and missing product deliveries[cite: 20].
            * **Ethan Gardner:** Recommended converting fixed single-issue dropdowns into open-ended inputs to prevent constraining feedback[cite: 20]. Resulted in stakeholder requests for **Commission Tracking** and **Refund Macros**[cite: 20].
            * **Izzy Bledsoe:** Validated deep feature ranking; recommended optional flag criteria for non-applicable workflows[cite: 20].
            * **Daniel Parker:** Addressed layout consistency and field indentation alignment[cite: 20].
            """)

    with tab_sa2:
        st.header("2. Process Decomposition & Data Flow Diagrams (DFD)")

        col_dfd_l, col_dfd_r = st.columns(2)
        with col_dfd_l:
            st.markdown("#### Context Diagram (Level 0 - Legacy)")
            st.code("""
[ Customer ] ──( Order & Payment )──▶ [ 0: Order Spreadsheet ]
                                             │
      ┌────────────────┬─────────────────────┼────────────────────┐
      ▼                ▼                     ▼                    ▼
[ Receipt ]     [ Shipping Ticket ]    [ Card Deposits ]   [ Sales Report ]
      │                │                     │                    │
[ Customer ]     [ Shipping ]             [ Bank ]          [ Accounting ]
            """, language="text")
            st.caption("Legacy State: A central spreadsheet acts as a manual bottleneck across all functions[cite: 20].")

        with col_dfd_r:
            st.markdown("#### Diagram 0 (Proposed Modular System)")
            st.code("""
[ Customer ] ──( Order & Payment )──▶ [ 1.0: Log Sale ] ──▶ [ Bank ]
                                             │ (Sales Record)
                                             ▼
                                     [( D1: Orders Store )]
                                       │              │
                     ┌─────────────────┘              └──────────────────┐
                     ▼                                                   ▼
            [ 2.0: Ship Product ]                              [ 3.0: Produce Report ]
                     │ (Shipping Request)                                │
                     ▼                                                   ▼
               [ Shipping ]                                       [ Accounting ]
            """, language="text")
            st.caption("Target State: Isolated functional modules reading/writing to a centralized data store[cite: 20].")

        st.markdown("---")
        st.markdown("#### Level 1 DFD Explosion Workflows")

        exp_col1, exp_col2 = st.columns(2)
        with exp_col1:
            st.markdown("**Process 1.0: Log Sale (Explosion)**")
            st.markdown("""
            1. **1.1 Capture Sales Data:** Receive item, customer, and payment payload[cite: 20].
            2. **1.2 Validate Payment:** Transmit authorization request to Bank API; evaluate status[cite: 20].
            3. **1.3 Update Orders Database:** Write confirmed `SALES RECORD` into transactional storage[cite: 20].
            4. **1.4 Generate Customer Receipt:** Produce transaction confirmation and push receipt to Customer[cite: 20].
            """)

        with exp_col2:
            st.markdown("**Process 2.0: Ship Product (Explosion)**")
            st.markdown("""
            1. **2.1 Verify Order Readiness:** Poll `Orders Store` for valid, paid transactions[cite: 20].
            2. **2.2 Generate Shipping Label:** Query carrier API (USPS/UPS); capture tracking token[cite: 20].
            3. **2.3 Update Shipping Status:** Mutate database status to `Shipped` and trigger tracking notifications[cite: 20].
            """)

    with tab_sa3:
        st.header("3. UML Behavioral Diagrams & System Logic")

        st.markdown("#### Formal Decision Table: Fulfillment Dispatch Criteria")
        decision_data = {
            "Condition / Action": [
                "Condition: Sale is Logged?",
                "Condition: Payment Received & Approved?",
                "Condition: Shipping Label Created?",
                "Action: Ship Product",
                "Action: Hold / Do Not Ship"
            ],
            "Rule 1 (Happy Path)": ["Y", "Y", "Y", "✅ EXECUTE", "—"],
            "Rule 2 (Label Failure)": ["Y", "Y", "N", "—", "🛑 HOLD (Label Retry)"],
            "Rule 3 (Payment Failure)": ["Y", "N", "—", "—", "🛑 HOLD (Payment Denied)"]
        }
        st.table(pd.DataFrame(decision_data))

        st.markdown("---")
        st.markdown("#### UML Sequence Architecture: Order Authorization")
        st.code("""
Salesperson           Order System              Credit Card Gateway         Database
    │                      │                             │                     │
    ├─── submitSale() ────▶│                             │                     │
    │                      ├─── validatePayment() ──────▶│                     │
    │                      │◀── Approved / Denied ───────┤                     │
    │                      │                                                   │
    │                      ├─── finalizeOrder() ──────────────────────────────▶│
    │                      │◀── Write Success ─────────────────────────────────┤
    │                      │                                                   │
    │◀── Return Receipt ───┤                                                   │
        """, language="text")

    with tab_sa4:
        st.header("4. Database Normalization & 3NF Implementation")
        st.markdown("""
        Decomposed legacy multi-column records into **Third Normal Form (3NF)** in PostgreSQL, decoupling customers, sales reps, line items, and shipping tracking[cite: 20].
        """)

        st.markdown("#### Relational Entities & Structural Keys")
        st.markdown("""
        * **`orders`:** Primary transactional entity (`id` PK, `sale_date`, `location_enum`, `salesperson_id` FK, `status_enum`, `amount_paid`, `notes`)[cite: 20].
        * **`line_item` & `items`:** Resolves order-to-product cardinality (`line_item` PK/FK bridge tracking `orders_id`, `item_id`, `quantity`)[cite: 20].
        * **`shipping` & `shipping_method`:** Decoupled carrier metadata (`tracking_id`, `shipping_cost`, `shipping_method` PK)[cite: 20].
        * **`credit_card_log`:** Auditable, tokenized merchant authorization logs (`cc_validation`, `orders_id` FK)[cite: 20].
        * **`employee`:** Internal personnel mapping (`id` PK, `name`, `employee_type`)[cite: 20].
        """)

        st.markdown("#### Normalized Analytical View Query")
        st.code("""
SELECT 
    'Neal Kauffman' AS Generated_By,
    o.id AS order_id, 
    o.sale_date, 
    o.location,
    e.name AS salesperson, 
    i.name AS item_name, 
    o.status, 
    o.amount_paid,
    ccl.cc_validation, 
    s.shipping_method, 
    s.shipping_cost, 
    o.notes
FROM orders o
LEFT JOIN line_item li ON li.orders_id = o.id
LEFT JOIN items i ON i.id = li.item_id
LEFT JOIN credit_card_log ccl ON ccl.orders_id = o.id
LEFT JOIN shipping s ON s.orders_id = o.id
LEFT JOIN employee e ON e.id = o.salesperson_id;
        """, language="sql")

    with tab_sa5:
        st.header("5. Target AWS Cloud Architecture & Engineering Memo")

        st.markdown("""
        ### Technical Implementation Memo
        * **To:** Mackinac Gnomes Steering Committee[cite: 20]
        * **From:** Neal Kauffman, Systems Analyst[cite: 20]
        * **Date:** April 30, 2026[cite: 20]
        * **Subject:** Production System Architecture & Deployment Blueprint[cite: 20]
        """)

        arch_c1, arch_c2 = st.columns(2)
        with arch_c1:
            st.markdown("""
            #### Network Segmentation (Defense in Depth)
            * **Public Web Subnet:** Ingress through an AWS Application Load Balancer (ALB) enforcing SSL/TLS termination[cite: 20]. Web servers serve UI/mockup assets[cite: 20].
            * **Private Application Subnet:** API layer housing application logic, processing JSON transactions, and executing third-party API calls[cite: 20].
            * **Private Data Subnet:** Fully isolated PostgreSQL RDS tier with zero direct public internet ingress, accepting incoming traffic strictly on port 5432 from the Application Subnet[cite: 20].
            """)

        with arch_c2:
            st.markdown("""
            #### Elastic Scalability & Redundancy
            * **Application Load Balancer:** Automatically distributes traffic bursts during high-volume seasonal demand[cite: 20].
            * **Decoupled 3rd-Party Integration:** Offloads payment tokenization and dynamic shipping rate calculations to external webhooks, minimizing system state overhead[cite: 20].
            """)

    with tab_sa6:
        st.header("6. Work Breakdown Structure (WBS) & Timeline")
        
        wbs_data = [
            {"ID": 1, "Task Name": "Create Project Shell Documentation", "Start": "2/16/2026", "Finish": "2/16/2026", "Duration": "1 day", "Predecessors": "—"},
            {"ID": 2, "Task Name": "Survey Users & Requirements Gathering", "Start": "2/17/2026", "Finish": "2/23/2026", "Duration": "5 days", "Predecessors": "1FS"},
            {"ID": 3, "Task Name": "Create Preliminary Architecture Plan", "Start": "2/17/2026", "Finish": "2/18/2026", "Duration": "2 days", "Predecessors": "1FS"},
            {"ID": 4, "Task Name": "Produce Data Flow Diagrams (Context, DFD 0, L1)", "Start": "2/24/2026", "Finish": "2/27/2026", "Duration": "4 days", "Predecessors": "2FS, 3FS"},
            {"ID": 5, "Task Name": "Produce UML Diagrams (Use Case, Activity, Sequence)", "Start": "2/19/2026", "Finish": "2/24/2026", "Duration": "4 days", "Predecessors": "3FS"},
            {"ID": 6, "Task Name": "Stakeholder Feedback & Diagram Revision", "Start": "3/2/2026", "Finish": "3/9/2026", "Duration": "6 days", "Predecessors": "4FS, 5FS"},
            {"ID": 7, "Task Name": "Create UI Wireframes & Mockups", "Start": "3/5/2026", "Finish": "3/12/2026", "Duration": "6 days", "Predecessors": "6FS"},
            {"ID": 8, "Task Name": "Produce 3NF ERD & SQL Data DDL", "Start": "3/5/2026", "Finish": "3/11/2026", "Duration": "5 days", "Predecessors": "6FS"},
            {"ID": 9, "Task Name": "Produce Cloud System Architecture Specification", "Start": "3/12/2026", "Finish": "3/17/2026", "Duration": "4 days", "Predecessors": "6FS, 8FS"},
            {"ID": 10, "Task Name": "Executive Presentation & Recording", "Start": "3/5/2026", "Finish": "3/25/2026", "Duration": "15 days", "Predecessors": "6FS"},
            {"ID": 11, "Task Name": "Warranty & Hypercare Support", "Start": "3/26/2026", "Finish": "4/6/2026", "Duration": "8 days", "Predecessors": "10FS"}
        ]
        
        st.dataframe(pd.DataFrame(wbs_data), hide_index=True, use_container_width=True)

elif page == "More Coming Soon!":
    st.title("🎬 Case Studies")
    st.divider()
    
    # Visual placeholder for under construction
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("") # Spacing
        st.write("")
        st.markdown("<h2 style='text-align: center;'>🚧 Under Construction</h2>", unsafe_allow_html=True)
        st.write("")
        st.info("I am currently cleaning and documenting new datasets for my next case study. Check back soon for deep dives into sales forecasting and healthcare analytics!")
        
        # Adding a loading spinner look-alike for effect
        st.write("---")
        st.caption("Status: Data Cleaning in Progress...")
        st.progress(65)

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
