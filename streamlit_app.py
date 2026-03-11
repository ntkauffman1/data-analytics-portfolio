import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(page_title="Neal Kauffman | Data Portfolio", page_icon="📊", layout="wide")

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

# Category Dropdown
category = st.sidebar.selectbox("Choose a Section:", 
    ["Main", "Games/Apps", "Case Studies", "Resources"]
)

# Sub-page routing based on the chosen category
if category == "Main":
    page = st.sidebar.radio("Go to:", ["Home", "About Me"])
elif category == "Games/Apps":
    page = st.sidebar.radio("Go to:", ["Trivia Scoreboard", "Alien Invasion Game"])
elif category == "Case Studies":
    page = st.sidebar.radio("Go to:", ["IMDB Insights"])
elif category == "Resources":
    page = st.sidebar.radio("Go to:", ["Reference Guide"])


# --- 3. PAGE LOGIC ---

if page == "Home":
    st.title("📊 Neal Kauffman: Data Analytics Portfolio")
    st.markdown("""
    Welcome! I am a **Computer Systems** student at Collin College transitioning into 
    Data Analytics. This site showcases my work in **Python**, **SQL**, and **Web Analysis**.
    """)

elif page == "About Me":
    st.title("👨‍💻 About Me")
    # 1. ADD YOUR PHOTO HERE
    # Ensure this filename EXACTLY matches the file in your folder!
    # I included a try/except block so your app won't crash if the file is missing locally.
    photo_filename = "495352114_10162816845657138_4891462490022732075_n.jpg"
    
    try:
        st.image(photo_filename, caption="Neal Kauffman", width=250)
    except FileNotFoundError:
        st.error(f"Image not found. Please place '{photo_filename}' in your VS Code folder.")
    st.markdown("""
    I am currently an Online Data Researcher with a strong foundation in Python and SQL. 
    
    Before pursuing my degree in Computer Systems and transitioning into data analytics, I spent several years managing fast-paced environments in the restaurant industry as a Front of House Manager and Bartender. 
    
    This background gave me a unique perspective on customer experience, daily operations, and the critical importance of making accurate, data-driven business decisions to improve efficiency.
    """)

elif page == "Trivia Scoreboard":
    # --- STEP 1: TEAM COUNT SCREEN ---
    if st.session_state.step == 1:
        st.title("🏆 Game Setup")
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

elif page == "IMDB Insights":
    st.title("🎬 Case Study: IMDB Data Warehouse")
    
    st.markdown("""
    ### Project Overview
    This project demonstrates the extraction, transformation, and loading (ETL) of IMDB movie data into a relational database. 
    I utilized **SQL Server (T-SQL)** to clean dirty CSV data, handle string conversions, remove duplicates, and build a normalized Data Warehouse view for Power BI.
    """)
    st.divider()
    
    st.subheader("🔍 SQL Portfolio Showcase")
    st.write("Select a script below to see the T-SQL logic I wrote, followed by a live preview of the cleaned dataset:")
    
    query_selection = st.selectbox("Select Script:", [
        "1. ETL: Dynamic Data Cleaning (Votes)",
        "2. Analysis: The Decade Trend",
        "3. Analysis: Genre Dominance",
        "4. ETL: The Final Power BI View"
    ])
    
    import sqlite3
    import os
    import pandas as pd
    
    # --- AUTO-BUILD THE DATABASE ---
    if not os.path.exists('imdb.db'):
        try:
            raw_df = pd.read_csv('IMBD_Final_CSV.csv')
            
            raw_df.columns = raw_df.columns.str.strip()
            
            # THE BUG FIX: SQLite crashes if it sees 'title' and 'Title'. We drop the lowercase one.
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
        
        # --- SCRIPT 1: DATA CLEANING ---
        if query_selection == "1. ETL: Dynamic Data Cleaning (Votes)":
            st.markdown("**Objective:** Convert a dirty string column containing 'M' (millions) and 'K' (thousands) into a usable numeric format for aggregation.")
            
            st.code('''
            -- Run the update logic to convert K/M suffixes into real numbers
            UPDATE Movies
            SET Votes_Clean = CASE 
                WHEN Votes LIKE '%M' THEN TRY_CAST(REPLACE(Votes, 'M', '') AS DECIMAL(10,2)) * 1000000
                WHEN Votes LIKE '%K' THEN TRY_CAST(REPLACE(Votes, 'K', '') AS DECIMAL(10,2)) * 1000
                ELSE TRY_CAST(REPLACE(Votes, ',', '') AS DECIMAL(10,2))
            END;
            ''', language='sql')
            
            st.markdown("**Live Result:** *(Notice the cleaned 'Votes' and Popularity columns from the final dataset)*")
            
            # MATCHING YOUR EXACT CSV COLUMNS
            query = 'SELECT Title, "Start Year", Votes, "Popularity Tier" FROM movies LIMIT 15'
            df = pd.read_sql_query(query, conn)
            st.dataframe(df, use_container_width=True)
            
        # --- SCRIPT 2: DECADE TREND ---
        elif query_selection == "2. Analysis: The Decade Trend":
            st.markdown("**Objective:** Group movies by decade using mathematical functions to see if average ratings change over time.")
            
            st.code('''
            -- Using Math (FLOOR) to group years into bins (e.g., 1994 becomes 1990)
            SELECT 
                FLOOR(Start_Year / 10) * 10 AS Decade,
                COUNT(*) AS Total_Movies,
                CAST(AVG(Rating) AS DECIMAL(10,2)) AS Avg_Rating
            FROM Movies
            WHERE Start_Year IS NOT NULL
            GROUP BY FLOOR(Start_Year / 10) * 10
            ORDER BY Decade DESC;
            ''', language='sql')
            
            # USING YOUR EXISTING DECADE COLUMN
            query = 'SELECT Decade, COUNT(*) AS Total_Movies, ROUND(AVG(Rating), 2) AS Avg_Rating FROM movies WHERE Decade IS NOT NULL GROUP BY Decade ORDER BY Decade DESC'
            df = pd.read_sql_query(query, conn)
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.dataframe(df, use_container_width=True)
            with col2:
                st.line_chart(data=df.set_index('Decade')['Avg_Rating'])

        # --- SCRIPT 3: GENRE DOMINANCE ---
        elif query_selection == "3. Analysis: Genre Dominance":
            st.markdown("**Objective:** Identify which genres produce the most content and calculate their average quality.")
            
            st.code('''
            -- Which genres produce the most content?
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
            with col1:
                st.dataframe(df, use_container_width=True)
            with col2:
                st.bar_chart(data=df.set_index('Genre')['Movie_Count'])

        # --- SCRIPT 4: THE FINAL VIEW ---
        elif query_selection == "4. ETL: The Final Power BI View":
            st.markdown("**Objective:** Create a clean, standardized View that Power BI can connect to directly, ensuring 100% data integrity.")
            
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
                REPLACE(REPLACE(Description, CHAR(13), ''), CHAR(10), '') AS Cleaned_Description,
                Stars
            FROM Movies;
            ''', language='sql')
            
            st.markdown("**Final Power BI Dataset Preview:**")
            df = pd.read_sql_query("SELECT * FROM movies LIMIT 100", conn)
            st.dataframe(df, use_container_width=True)
            
        conn.close()
        
    except Exception as e:
        st.error(f"Error loading data: {e}")

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
