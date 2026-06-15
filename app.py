"""
🎬 Movie Recommender AI - Streamlit App
Dark theme UI for content-based movie recommendations.
Uses TF-IDF Cosine Similarity under the hood via recommender.py
"""

import streamlit as st
from recommender import recommend  # Your existing recommender module

# ─────────────────────────────────────────────
# PAGE CONFIG — must be the very first Streamlit call
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Movie Recommender AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"   # Force sidebar open on load
)

# ─────────────────────────────────────────────
# CUSTOM CSS — dark theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Global Reset ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0B0B0B;
        color: #FFFFFF;
    }

    /* ── App background ── */
    .stApp {
        background-color: #0B0B0B;
    }

    /* ── Hide Streamlit default footer & deploy button only ── */
    /* NOTE: Do NOT hide 'header' — it contains the sidebar toggle button */
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    [data-testid="stToolbar"] { visibility: hidden; }

    /* Style the top header bar to blend with dark theme */
    [data-testid="stHeader"] {
        background-color: #0B0B0B;
        border-bottom: 1px solid #1a1a1a;
    }

    /* Make the sidebar toggle (hamburger) icon visible and red-tinted */
    [data-testid="collapsedControl"] {
        color: #E50914 !important;
    }

    /* ── Sidebar styling ── */
    [data-testid="stSidebar"] {
        background-color: #111111;
        border-right: 1px solid #2a2a2a;
    }
    [data-testid="stSidebar"] h2 {
        color: #E50914;
        font-size: 1.1rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li {
        color: #AAAAAA;
        font-size: 0.88rem;
        line-height: 1.7;
    }

    /* ── Header section ── */
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #FFFFFF;
        text-align: center;
        margin-top: 1.5rem;
        margin-bottom: 0.25rem;
        line-height: 1.1;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #AAAAAA;
        text-align: center;
        margin-bottom: 1.2rem;
        font-weight: 300;
    }

    /* ── Tech badges ── */
    .badge-row {
        display: flex;
        justify-content: center;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin-bottom: 2.2rem;
    }
    .badge {
        background-color: #1e1e1e;
        border: 1px solid #333;
        border-radius: 999px;
        padding: 0.25rem 0.85rem;
        font-size: 0.75rem;
        color: #AAAAAA;
        font-weight: 500;
        letter-spacing: 0.04em;
    }

    /* ── Divider ── */
    .red-divider {
        width: 60px;
        height: 3px;
        background: #E50914;
        border-radius: 2px;
        margin: 0 auto 2rem auto;
    }

    /* ── Search input override ── */
    .stTextInput > div > div > input {
        background-color: #151515 !important;
        border: 1.5px solid #2a2a2a !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
        font-size: 1rem !important;
        padding: 0.75rem 1rem !important;
        transition: border-color 0.2s ease;
    }
    .stTextInput > div > div > input:focus {
        border-color: #E50914 !important;
        box-shadow: 0 0 0 2px rgba(229, 9, 20, 0.15) !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #555 !important;
    }
    .stTextInput label {
        color: #AAAAAA !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
    }

    /* ── Primary button (Get Recommendations) ── */
    .stButton > button {
        background: #E50914 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.04em !important;
        padding: 0.65rem 2rem !important;
        width: 100% !important;
        transition: background 0.2s ease, transform 0.1s ease, box-shadow 0.2s ease !important;
        cursor: pointer !important;
    }
    .stButton > button:hover {
        background: #b20710 !important;
        box-shadow: 0 4px 20px rgba(229, 9, 20, 0.35) !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button:active {
        transform: translateY(0px) !important;
    }

    /* ── Results heading ── */
    .results-heading {
        font-size: 1.5rem;
        font-weight: 700;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 0.3rem;
    }
    .results-heading span {
        color: #E50914;
    }
    .results-subtext {
        text-align: center;
        color: #AAAAAA;
        font-size: 0.85rem;
        margin-bottom: 1.8rem;
    }

    /* ── Movie card ── */
    .movie-card {
        background: #151515;
        border: 1px solid #2a2a2a;
        border-radius: 12px;
        padding: 1.4rem 1.1rem 1.2rem 1.1rem;
        min-height: 160px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        position: relative;
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        cursor: default;
    }
    .movie-card:hover {
        transform: translateY(-4px);
        border-color: #E50914;
        box-shadow: 0 0 20px rgba(229, 9, 20, 0.2), 0 8px 24px rgba(0,0,0,0.5);
    }

    /* Rank badge in top-left corner */
    .card-rank {
        position: absolute;
        top: 10px;
        left: 12px;
        font-size: 0.68rem;
        font-weight: 700;
        color: #E50914;
        background: rgba(229, 9, 20, 0.12);
        border-radius: 4px;
        padding: 2px 6px;
        letter-spacing: 0.05em;
    }
    /* Film icon */
    .card-icon {
        font-size: 1.8rem;
        margin-bottom: 0.6rem;
        opacity: 0.75;
    }
    /* Movie title */
    .card-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #FFFFFF;
        line-height: 1.3;
        margin-bottom: 0.6rem;
        word-wrap: break-word;
    }
    /* Thin red divider inside card */
    .card-divider {
        width: 32px;
        height: 2px;
        background: #E50914;
        border-radius: 1px;
        margin: 0 auto 0.55rem auto;
    }
    /* Caption */
    .card-caption {
        font-size: 0.7rem;
        color: #666;
        letter-spacing: 0.03em;
        line-height: 1.4;
    }

    /* ── Footer ── */
    .footer {
        text-align: center;
        color: #444;
        font-size: 0.8rem;
        margin-top: 3.5rem;
        padding-bottom: 1.5rem;
        border-top: 1px solid #1a1a1a;
        padding-top: 1.2rem;
    }
    .footer span {
        color: #E50914;
    }

    /* ── Streamlit alert overrides ── */
    .stWarning, .stError {
        border-radius: 8px !important;
    }

    /* ── Column gaps ── */
    [data-testid="column"] {
        padding: 0 0.3rem !important;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR — About section
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎬 About")
    st.markdown("""
This is a **Content-Based Recommendation System** built using:

- 📐 TF-IDF Vectorization
- 📏 Cosine Similarity
- 🐼 Pandas
- 🤖 Scikit-Learn
- ⚡ Streamlit

---
Enter any movie title in the search bar and the model will find the 5 most similar movies based on content features.
    """)
    st.markdown("---")
    st.markdown("<p style='color:#555;font-size:0.75rem;'>Version 1.0 • Content-Based Filtering</p>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HEADER — Title, subtitle, and tech badges
# ─────────────────────────────────────────────
st.markdown('<div class="hero-title">🎬 Movie Recommender AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">Find movies similar to your favorites using Machine Learning</div>',
    unsafe_allow_html=True
)

# Tech badges row
st.markdown("""
<div class="badge-row">
    <span class="badge">TF-IDF Cosine Similarity</span>
    <span class="badge">Python</span>
    <span class="badge">Streamlit</span>
    <span class="badge">Scikit-Learn</span>
    <span class="badge">Content-Based</span>
</div>
""", unsafe_allow_html=True)

# Thin red accent divider under header
st.markdown('<div class="red-divider"></div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SEARCH SECTION — Centered input + button
# ─────────────────────────────────────────────
# Use columns to center the search UI (1:2:1 ratio)
_, center_col, _ = st.columns([1, 2, 1])

with center_col:
    # Text input for the movie name
    movie_input = st.text_input(
        label="Movie Title",
        placeholder="Search for a movie like Inception...",
        label_visibility="collapsed"   # Hide label visually; kept for accessibility
    )

    # Red "Get Recommendations" button
    search_clicked = st.button("🔍  Get Recommendations", use_container_width=True)


# ─────────────────────────────────────────────
# OUTPUT SECTION — Recommendation cards
# ─────────────────────────────────────────────
if search_clicked:
    # ── Guard: empty input ──
    if not movie_input.strip():
        st.warning("⚠️  Please enter a movie name.")

    else:
        # Call the recommend function from recommender.py
        # Expected return: list of 5 movie title strings, or empty list if not found
        try:
            recommendations = recommend(movie_input.strip())
        except Exception:
            # Catch any unexpected errors from the recommender module
            recommendations = []

        # ── Guard: movie not found ──
        if not recommendations:
            st.error(f"❌  **'{movie_input}'** was not found in our database. Please check the spelling or try another title.")

        else:
            # ── Results heading ──
            st.markdown(
                f'<div class="results-heading">Because you watched <span>{movie_input.title()}</span></div>',
                unsafe_allow_html=True
            )
            st.markdown(
                '<div class="results-subtext">Top 5 picks matched by TF-IDF content similarity</div>',
                unsafe_allow_html=True
            )

            # ── 5 movie cards in a single row ──
            cols = st.columns(5)   # Create 5 equal-width columns

            for i, (col, title) in enumerate(zip(cols, recommendations), start=1):
                with col:
                    # Render each movie as a styled HTML card
                    st.markdown(f"""
                    <div class="movie-card">
                        <div class="card-rank">#{i}</div>
                        <div class="card-icon">🎬</div>
                        <div class="card-title">{title}</div>
                        <div class="card-divider"></div>
                        <div class="card-caption">Recommended using<br>TF-IDF similarity</div>
                    </div>
                    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Made with <span>❤️</span> using Python &amp; Machine Learning
</div>
""", unsafe_allow_html=True)
