import streamlit as st
import pandas as pd
import sqlite3
import os
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(page_title="Neal Kauffman | Data Portfolio", page_icon="📊", layout="wide")

# --- CUSTOM CSS FOR HIGH-VISIBILITY TABS ---
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

# ADDED "Site Architecture" to the end of the categories
category = st.sidebar.selectbox("Choose a Section:", 
    ["Main", "Games/Apps", "Case Studies", "Resources", "Site Architecture"]
)

if category == "Main":
    page = st.sidebar.radio("Go to:", ["Home", "About Me"])
elif category == "Games/Apps":
    page = st.sidebar.radio("Go to:", ["Trivia Scoreboard", "Alien Invasion Game"])
elif category == "Case Studies":
    page = st.sidebar.radio("Go to:", ["IMDB Insights"])
elif category == "Resources":
    page = st.sidebar.radio("Go to:", ["Reference Guide"])
elif category == "Site Architecture":
    # CREATED NEW ROUTE FOR SYSTEM HEALTH
    page = st.sidebar.radio("Go to:", ["System Health", "Tech Stack"])

# --- SYSTEM HEALTH TEASER ---
st.sidebar.markdown("---")
st.sidebar.markdown("🟢 **System Status:** All apps online")
st.sidebar.caption("CI/CD Pipeline: Active | Uptime: 99.9%")

# --- PAGE LOGIC ---

if page == "Home":
    st.title("Welcome to My Data Portfolio")
    st.markdown("""
    ### Hello! I'm Neal Kauffman. **Computer Systems** Student at Collin College Transitioning into Data Analytics.
    This portfolio is a live demonstration of my skills in **Data Analysis, SQL Transformation, Data Visualization and Python Development.**
    
    Use the navigation menu on the left to explore:
    - **IMDB Insights:** A full ETL pipeline from Excel to SQL and Power BI.
    - **Interactive Apps:** Custom-built Python tools like the Trivia Scoreboard.
    - **Game Dev:** Logic and structure for a Python-based space shooter.
    """)
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
