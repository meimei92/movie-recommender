# Step 1: Import pandas library for working with data
import pandas as pd

# ─────────────────────────────────────────────
# Step 2: Load both CSV files into DataFrames
# ─────────────────────────────────────────────

# Load the movies dataset (contains info like title, overview, genres, etc.)
movies = pd.read_csv("data/tmdb_5000_movies.csv")

# Load the credits dataset (contains cast and crew information)
credits = pd.read_csv("data/tmdb_5000_credits.csv")

# ─────────────────────────────────────────────
# Step 3: Merge both datasets on the 'title' column
# This combines rows where the movie title matches in both files
# ─────────────────────────────────────────────
df = pd.merge(movies, credits, on="title")

# Print total number of movies BEFORE cleaning
print(f"Number of movies before cleaning: {len(df)}")

# ─────────────────────────────────────────────
# Step 4: Keep only the columns we need
# 'title'    → name of the movie
# 'overview' → short description / plot summary
# ─────────────────────────────────────────────
df = df[["title", "overview"]]

# ─────────────────────────────────────────────
# Step 5: Remove rows that have null (missing) values
# dropna() removes any row where at least one column is empty
# ─────────────────────────────────────────────
df = df.dropna()

# ─────────────────────────────────────────────
# Step 6: Remove duplicate movie titles
# keep="first" keeps the first occurrence and drops the rest
# ─────────────────────────────────────────────
df = df.drop_duplicates(subset="title", keep="first")

# Print total number of movies AFTER cleaning
print(f"Number of movies after cleaning : {len(df)}")

# ─────────────────────────────────────────────
# Step 7: Save the cleaned DataFrame to a new CSV file
# index=False prevents pandas from writing row numbers into the file
# ─────────────────────────────────────────────
df.to_csv("cleaned_movies.csv", index=False)

print("✅ Cleaned data saved to cleaned_movies.csv")