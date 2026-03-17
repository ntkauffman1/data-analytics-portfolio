/* ==========================================================================
   Project: IMDB Data Analytics Pipeline (ETL & Analysis)
   Author:  Neal Kauffman
   Date:    December 2025
   Description: End-to-end SQL transformation script that replicates Excel-based logic to convert raw, 
                dirty CSV data into a normalized Data Warehouse for Power BI.
   
   OBJECTIVES:
   1. Ingest raw CSV data.
   2. Clean formatting errors (commas, hidden characters).
   3. Create new calculated columns for analysis.
   4. Create a clean View for Power BI ingestion.
   ========================================================================== */
/* 
   --------------------------------------------------------------------------
   PROBLEM STATEMENT (The "Dirty" Data):
   1. Inconsistent Data Types: The 'Votes' column contained mixed formats 
      (e.g., '1.5M', '350K', '1,200'), preventing mathematical aggregation.
   2. Duplicate Records: Titles were re-uploaded with identical metadata.
   3. Formatting Errors: Hidden Carriage Returns (CHAR 13) and Line Feeds 
      in descriptions broke CSV delimiters and export logic.
   4. Logic Gaps: No standardized definition existed for "High vs Low" popularity.

   RESOLUTIONS APPLIED:
   1. Dynamic Cleaning: Implemented CASE logic to parse 'K'/'M' suffixes and 
      convert strings into a CAST(DECIMAL) format (Votes_Clean).
   2. Deduplication: Utilized Common Table Expressions (CTEs) with ROW_NUMBER() 
      window functions to isolate and delete duplicate entities.
   3. Sanitization: Applied NESTED REPLACE() functions to strip invisible characters.
   4. Abstraction: Encapsulated final logic in a View (v_Master_Movies) to 
      serve as a "Clean Connector" for Power BI, ensuring 100% data integrity.
   ========================================================================== */

USE IMDB_Project;
GO


/* --------------------------------------------------------------------------
   PART 1: DATA INSPECTION & CLEANING
   -------------------------------------------------------------------------- */

-- Task 1: Inspect Titles for extra spaces
-- We use TRIM to remove leading/trailing spaces.
-- We use UPPER because SQL Server lacks a PROPER() case function.
SELECT TOP 50
    Title AS Original_Raw_Title,
    TRIM(Title) AS Cleaned_Title,
    UPPER(TRIM(Title)) AS Standardized_Title
FROM Movies;

-- Task 2: Identify Duplicates
-- Finding records that share the same Title and Start Year.
-- This helps us identify if a movie was uploaded twice.
SELECT 
    Title, 
    [Start_Year], 
    COUNT(*) AS Record_Count
FROM Movies
GROUP BY Title, [Start_Year]
HAVING COUNT(*) > 1  -- Only show groups that appear more than once
ORDER BY Record_Count DESC;

/* --------------------------------------------------------------------------
   PART 1.5: THE CLEANING EXECUTION (The "Heavy Lifting")
   -------------------------------------------------------------------------- */

-- Task A: Standardize the "Votes" Column
-- The raw data had strings like '1.5M', '300K', and '1,200'.
-- We need to clean this into a purely numeric column (Votes_Clean).

-- 1. Create the new column ONLY if it doesn't exist yet (Prevents Error Msg 2705)
IF COL_LENGTH('Movies', 'Votes_Clean') IS NULL
BEGIN
    ALTER TABLE Movies ADD Votes_Clean DECIMAL(10,2);
END
GO

-- 2. Run the update logic to convert K/M suffixes into real numbers
UPDATE Movies
SET Votes_Clean = CASE 
    -- Case 1: Millions (e.g., '1.5M' -> 1500000)
    WHEN Votes LIKE '%M' THEN TRY_CAST(REPLACE(Votes, 'M', '') AS DECIMAL(10,2)) * 1000000
    
    -- Case 2: Thousands (e.g., '300K' -> 300000)
    WHEN Votes LIKE '%K' THEN TRY_CAST(REPLACE(Votes, 'K', '') AS DECIMAL(10,2)) * 1000
    
    -- Case 3: Regular numbers with commas (e.g., '1,200' -> 1200)
    ELSE TRY_CAST(REPLACE(Votes, ',', '') AS DECIMAL(10,2))
END;

-- Task B: Remove Duplicate Records
-- We use a CTE (Common Table Expression) to identify and DELETE duplicates,
-- keeping only the first instance of every Title+Year combination.
WITH Duplicate_CTE AS (
    SELECT 
        Title, 
        Start_Year, 
        ROW_NUMBER() OVER(PARTITION BY Title, Start_Year ORDER BY Title) AS RowNum
    FROM Movies
)
-- Switch "SELECT * " to "DELETE" to actually remove them
DELETE FROM Duplicate_CTE
WHERE RowNum > 1;

-- Task C: Handle Nulls
-- Remove entries that are useless for analysis (Records with No Rating or No Year)
-- Without a year or rating, we cannot plot them on the dashboard.
DELETE FROM Movies
WHERE Rating IS NULL OR Start_Year IS NULL;

-- Task D: Fix Title Formatting
-- Permanently update the Title column to remove extra spaces we found in Task 1.
UPDATE Movies
SET Title = TRIM(Title);

/* --------------------------------------------------------------------------
   PART 1C: EXCEL PIVOT TABLE REPLICATION (Genre Logic)
   -------------------------------------------------------------------------- */

-- Task: Validate Genre Distribution
-- In Excel, we used a Pivot Table to see which Genres had the most rows.
-- We replicate that here to ensure SQL matches our Excel findings.
-- This acts as a "Sanity Check" before we build the final View.

SELECT 
    Genre,
    COUNT(*) AS Count_of_Titles,
    -- We verify if the Average Rating aligns with our Excel pivot (e.g., Drama ~6.8)
    CAST(AVG(Rating) AS DECIMAL(10,2)) AS Avg_Rating,
    -- We check the Total Volume of engagement
    FORMAT(SUM(Votes_Clean), 'N0') AS Total_Votes
FROM Movies
WHERE Genre IS NOT NULL
GROUP BY Genre
ORDER BY Count_of_Titles DESC;

/* --------------------------------------------------------------------------
   PART 2: DATA TRANSFORMATION & LOGIC
   -------------------------------------------------------------------------- */

-- Task 3: Text Cleaning (Descriptions)
-- Removing hidden "Carriage Returns" (CHAR(13)) and "Line Feeds" (CHAR(10))
-- that often break exports to Excel/CSV.
SELECT TOP 20
    Description AS Original_Desc,
    REPLACE(REPLACE(Description, CHAR(13), ''), CHAR(10), '') AS Cleaned_Desc
FROM Movies;

-- Task 4: Business Logic (Categorization)
-- Replicating the "IF" logic from Excel to categorize movies by popularity.
-- Logic: High (>10k votes), Medium (1k-10k), Low (<1k).
SELECT 
    Title,
    Votes_Clean,
    CASE
        WHEN Votes_Clean >= 10000 THEN 'High Popularity'
        WHEN Votes_Clean >= 1000 THEN 'Medium Popularity'
        ELSE 'Low Popularity'
    END AS Popularity_Category
FROM Movies;

/* --------------------------------------------------------------------------
   PART 3: AGGREGATION & ANALYSIS
   -------------------------------------------------------------------------- */

-- Task 5: The "Decade" Trend
-- Using CAST(AS DECIMAL(10,2)) to force the average to 2 decimal places.
-- We use Math (FLOOR) to group years into bins (e.g., 1994 becomes 1990).
-- This answers: "Are movies getting better or worse over time?"
SELECT 
    FLOOR(Start_Year / 10) * 10 AS Decade,
    COUNT(*) AS Total_Movies,
    CAST(AVG(Rating) AS DECIMAL(10,2)) AS Avg_Rating
FROM Movies
WHERE Start_Year IS NOT NULL
GROUP BY FLOOR(Start_Year / 10) * 10
ORDER BY Decade DESC;

-- Task 6: Genre Dominance
-- Which genres produce the most content?
-- We calculate the Count and the Average Rating to see Quantity vs Quality.
SELECT TOP 10
    Genre,
    COUNT(*) AS Movie_Count,
    CAST(AVG(Rating) AS DECIMAL(10,2)) AS Genre_Avg_Rating
FROM Movies
GROUP BY Genre
ORDER BY Movie_Count DESC;

/* --------------------------------------------------------------------------
   PART 4: THE FINAL VIEW (POWER BI CONNECTOR)
   -------------------------------------------------------------------------- */

-- This VIEW acts as the "Clean Table" for Power BI.
-- It applies all our cleaning rules automatically so Power BI never sees dirty data.
GO

CREATE OR ALTER VIEW v_Master_Movies AS
SELECT
    -- 1. Identity Columns
    Title,
    
    -- 2. Cleaned Dates
    Start_Year,
    FLOOR(Start_Year / 10) * 10 AS Decade,
    
    -- 3. Cleaned Metrics
    -- CAST added here to ensure Rating is always 2 decimals (e.g., 7.50)
    CAST(Rating AS DECIMAL(10,2)) AS Rating,
    Votes_Clean AS Votes, 
    
    -- 4. Text & Categories
    TRIM(Genre) AS Genre,
    CASE
        WHEN Votes_Clean >= 10000 THEN 'High Popularity'
        WHEN Votes_Clean >= 1000 THEN 'Medium Popularity'
        ELSE 'Low Popularity'
    END AS Popularity_Category,
    
    -- 5. Metadata
    REPLACE(REPLACE(Description, CHAR(13), ''), CHAR(10), '') AS Cleaned_Description,
    Stars

FROM Movies;
GO

-- Final Verification: Run this to confirm the View works
SELECT TOP 100 * FROM v_Master_Movies;