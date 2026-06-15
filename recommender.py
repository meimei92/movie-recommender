# ─────────────────────────────────────────────────────────────
# Movie Recommendation System using TF-IDF + Cosine Similarity
# ─────────────────────────────────────────────────────────────
#
# How it works (big picture):
#   1. Convert every movie's overview text into a numeric vector
#      using TF-IDF (Term Frequency–Inverse Document Frequency).
#   2. Measure how "close" two vectors are using Cosine Similarity.
#   3. For a given movie, return the 5 closest neighbours.
#
# Time Complexity (brief):
#   - TF-IDF fitting   : O(N * W)  — N movies, W unique words
#   - Cosine similarity: O(N²* F)  — F = max_features (5000)
#   - recommend()      : O(N log N) per query (sorting)
# ─────────────────────────────────────────────────────────────

# Step 1: Import required libraries
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ─────────────────────────────────────────────────────────────
# Step 2: Load the cleaned dataset
# ─────────────────────────────────────────────────────────────

df = pd.read_csv("cleaned_movies.csv")

# Reset index so row numbers are clean (0, 1, 2, …)
df = df.reset_index(drop=True)


# ─────────────────────────────────────────────────────────────
# Step 3: Build the TF-IDF matrix
#
# What is TF-IDF?
#   • TF  (Term Frequency)         — how often a word appears in ONE movie's overview.
#   • IDF (Inverse Document Freq.) — penalises words that appear in EVERY movie
#                                    (e.g. "the", "a", "movie") so they carry less weight.
#   • Together they highlight words that are *unique* to each movie.
#
# Why remove stop words?
#   Words like "the", "is", "and", "a" appear in every text.
#   They add noise without meaning. stop_words='english' removes ~318 such words
#   so that only meaningful words (e.g. "astronaut", "heist", "love") influence results.
#
# Why max_features=5000?
#   Limits vocabulary to the 5000 most important words, keeping memory usage low
#   while still capturing enough detail for good recommendations.
# ─────────────────────────────────────────────────────────────

vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)

# fit_transform does two things:
#   fit()      → learns the vocabulary from all overviews
#   transform()→ converts each overview into a numeric vector
# Result shape: (number_of_movies, 5000) — one row per movie, one column per word
tfidf_matrix = vectorizer.fit_transform(df["overview"])


# ─────────────────────────────────────────────────────────────
# Step 4: Compute Cosine Similarity
#
# What is Cosine Similarity?
#   It measures the ANGLE between two vectors (not their size).
#   • Score = 1.0 → identical direction → very similar content
#   • Score = 0.0 → perpendicular      → completely unrelated
#
#   Formula:  similarity = (A · B) / (|A| * |B|)
#
#   Using angle (not length) is ideal for text because a long overview
#   and a short one can still be very similar in topic.
#
# Result: an (N x N) matrix where cell [i][j] is the similarity
#         between movie i and movie j.
# ─────────────────────────────────────────────────────────────

similarity = cosine_similarity(tfidf_matrix)


# ─────────────────────────────────────────────────────────────
# Step 5: Build a title → index lookup (case-insensitive search)
#
# We store lowercase titles so we can look up "inception",
# "INCEPTION", or "Inception" and always find the right row.
# ─────────────────────────────────────────────────────────────

# Map lowercase title → DataFrame index
title_to_index = {title.lower(): idx for idx, title in enumerate(df["title"])}


# ─────────────────────────────────────────────────────────────
# Step 6: The recommend() function
# ─────────────────────────────────────────────────────────────

def recommend(movie_name):
    """
    Returns a list of 5 movie titles similar to movie_name.

    Parameters
    ----------
    movie_name : str
        Title of the movie to base recommendations on.

    Returns
    -------
    list[str]
        Top 5 similar movie titles, or ["Movie not found"] if unknown.
    """

    # ── 6a. Case-insensitive lookup ──────────────────────────
    movie_key = movie_name.lower().strip()

    if movie_key not in title_to_index:
        # Movie doesn't exist in our dataset — return a friendly message
        return ["Movie not found"]

    # Get the integer row index of the requested movie
    movie_idx = title_to_index[movie_key]

    # ── 6b. Retrieve similarity scores ──────────────────────
    # similarity[movie_idx] is a 1-D array of length N,
    # where each value is how similar that movie is to ours.
    scores = list(enumerate(similarity[movie_idx]))
    # scores looks like: [(0, 0.12), (1, 0.87), (2, 0.03), …]
    #                      ↑ index    ↑ similarity score

    # ── 6c. Sort by similarity score (descending) ────────────
    #
    # How sorting works here:
    #   sorted(..., key=lambda x: x[1], reverse=True)
    #   • lambda x: x[1]  → sort by the SCORE (second element of the tuple)
    #   • reverse=True     → highest score first
    #
    # Time: O(N log N) — standard comparison sort
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

    # ── 6d. Exclude the movie itself ─────────────────────────
    # The movie will always be most similar to itself (score = 1.0),
    # so we skip any tuple whose index equals movie_idx.
    top_movies = [
        df.iloc[idx]["title"]
        for idx, score in sorted_scores
        if idx != movie_idx
    ][:5]   # Keep only the top 5

    return top_movies


# ─────────────────────────────────────────────────────────────
# Step 7: Test the recommender
# ─────────────────────────────────────────────────────────────

print("Recommendations for 'Inception':")
print(recommend("Inception"))

print("\nRecommendations for 'Avatar':")
print(recommend("Avatar"))

print("\nRecommendations for 'Titanic':")
print(recommend("Titanic"))