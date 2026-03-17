import pyodbc
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. SETUP THE CONNECTION

server = 'NTKCOMP\SQLEXPRESS_USE' 
database = 'IMDB_Project'

print("Connecting to SQL Server...")
conn = pyodbc.connect(f'Driver={{SQL Server}};Server={server};Database={database};Trusted_Connection=yes;')

# 2. PULL THE DATA
# We only want the numeric columns for correlation
sql_query = """
SELECT 
    Rating, 
    Start_Year, 
    Votes_Clean AS Votes
FROM Movies
"""

print("Reading data...")
df = pd.read_sql(sql_query, conn)

# 3. CALCULATE CORRELATION
print("Calculating correlations...")
correlation_matrix = df.corr()

# 4. VISUALIZE IT
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('IMDB Movie Correlation Matrix')
plt.show()


# 5. SCATTER PLOT
plt.figure(figsize=(10, 6))

# Plot the dots
sns.scatterplot(data=df, x='Votes', y='Rating', alpha=0.3, color='blue')

# Add a title
plt.title('Do Popular Movies Get Better Ratings? (Correlation: 0.2)')
plt.xlabel('Number of Votes (Popularity)')
plt.ylabel('IMDB Rating (Quality)')
plt.grid(True, linestyle='--', alpha=0.5)

plt.show()