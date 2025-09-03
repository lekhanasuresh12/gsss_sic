import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- Streamlit Setup ----------------
st.set_page_config(page_title="Movie Ratings Project", layout="wide")

st.markdown("## 🎬 Movie Ratings Project Dashboard")
st.write("This app performs data cleaning, merging, pivot tables, and visualization.")

# ---------------- Load & Clean Data ----------------
@st.cache_data
def load_data():
    movies = pd.read_csv("movies.csv")
    ratings = pd.read_csv("ratings.csv")
    users = pd.read_csv("users.csv")

    # Clean & merge
    ratings['Rating'] = ratings['Rating'].fillna(0)
    movies = movies.drop_duplicates()
    ratings = ratings.drop_duplicates()
    users = users.drop_duplicates()

    # Step 7 & 8: Merge datasets
    ratings_movies = pd.merge(ratings, movies, on="MovieID", how="inner")
    full_df = pd.merge(ratings_movies, users, on="UserID", how="inner")

    return movies, ratings, users, ratings_movies, full_df

movies, ratings, users, ratings_movies, full_df = load_data()

# ---------------- Verification ----------------
st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "Home",
        "Pivot Tables",
        "Movie Analysis",
        "User Analysis",
        "Genre Analysis",
        "Export Data"
    ]
)

# ---------------- Pivot Tables ----------------
pivot_movie = full_df.pivot_table(index="Title", values="Rating", aggfunc="mean")
pivot_genre = (
    full_df.assign(Genre=full_df['Genre'].str.split('|')).explode('Genre')
    .pivot_table(index="Genre", values="Rating", aggfunc="mean")
)
pivot_user = full_df.pivot_table(index="UserID", values="Rating", aggfunc="mean")

# Step 14: Movies with avg rating ≥ 4.0
high_rated_movies = pivot_movie[pivot_movie["Rating"] >= 4.0]

# Step 15: Users who rated more than 5 movies
user_counts = full_df.groupby("UserID").size()
active_users = user_counts[user_counts > 5]

# Step 16: Top 5 movies by number of ratings
movie_counts = full_df.groupby("Title").size().sort_values(ascending=False).head(5)

# Step 17: Movies with highest & lowest average ratings
highest_rated = pivot_movie["Rating"].idxmax(), pivot_movie["Rating"].max()
lowest_rated = pivot_movie["Rating"].idxmin(), pivot_movie["Rating"].min()

# Step 18: Add RatingCategory
full_df["RatingCategory"] = pd.cut(
    full_df["Rating"],
    bins=[0, 2.9, 3.9, 5],
    labels=["Low", "Medium", "High"]
)

# Step 19: Add IsPopular (movies with >10 ratings)
movie_rating_counts = full_df.groupby("Title")["Rating"].transform("count")
full_df["IsPopular"] = movie_rating_counts.apply(lambda x: "Yes" if x > 10 else "No")

# ---------------- Visualization Helpers ----------------
def plot_chart(df, title, xlabel, ylabel, top_n=None, color="skyblue"):
    if top_n:
        df = df.sort_values("Rating", ascending=False).head(top_n)
    else:
        df = df.sort_values("Rating", ascending=False)

    fig, ax = plt.subplots(figsize=(8,4))
    df.plot(kind="bar", ax=ax, color=color, legend=False)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=30, ha="right")
    st.pyplot(fig)

def plot_pie_chart(df, title):
    fig, ax = plt.subplots(figsize=(6,6))
    df.plot(kind="pie", y="Rating", ax=ax, autopct="%1.1f%%", legend=False)
    ax.set_ylabel("")
    ax.set_title(title)
    st.pyplot(fig)

# ---------------- Pages ----------------
if page == "Home":
    # Step 9: Merge Verification Section
    st.markdown("### ✅ Step 9: Merge Verification (Row Counts)")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Movies", movies.shape[0])
    col2.metric("Ratings", ratings.shape[0])
    col3.metric("Users", users.shape[0])
    col4.metric("Ratings+Movies", ratings_movies.shape[0])
    col5.metric("Full Merge (All)", full_df.shape[0])

    st.markdown("### Preview of Final Merged Data")
    st.dataframe(full_df, use_container_width=True)

elif page == "Pivot Tables":
    st.subheader("🎯 Pivot Tables")
    st.write("**Average Rating per Movie**")
    st.dataframe(pivot_movie.head(10))
    st.write("**Average Rating per Genre**")
    st.dataframe(pivot_genre)
    st.write("**Average Rating per User**")
    st.dataframe(pivot_user.head(10))

elif page == "Movie Analysis":
    st.subheader("🍿 Movie Analysis")
    st.write("**Top 10 Movies (Avg Rating)**")
    plot_chart(pivot_movie, "Top 10 Movies", "Movie", "Avg Rating", top_n=10)

    st.write("**Movies with Avg Rating ≥ 4.0**")
    st.dataframe(high_rated_movies)

    st.write("**Top 5 Movies by Number of Ratings**")
    st.dataframe(movie_counts)

    st.write(f"🏆 Highest Rated Movie: {highest_rated[0]} ({highest_rated[1]:.2f})")
    st.write(f"💔 Lowest Rated Movie: {lowest_rated[0]} ({lowest_rated[1]:.2f})")

elif page == "User Analysis":
    st.subheader("👤 User Analysis")
    st.write("**Top 10 Users by Avg Rating**")
    plot_chart(pivot_user, "Top 10 Users", "UserID", "Avg Rating", top_n=10, color="lightgreen")

    st.write("**Users who rated more than 5 movies**")
    st.dataframe(active_users)

elif page == "Genre Analysis":
    st.subheader("🎭 Genre Analysis")
    col1, col2 = st.columns(2)

    with col1:
        plot_chart(pivot_genre, "Average Rating per Genre", "Genre", "Avg Rating")
    with col2:
        plot_pie_chart(pivot_genre, "Genre Ratings Distribution")

    st.write("**Genre Table**")
    st.dataframe(pivot_genre)

elif page == "Export Data":
    st.subheader("📂 Export Data")

    # Step 20 & 21: Export CSVs
    pivot_movie.to_csv("movie_avg_ratings.csv")
    pivot_genre.to_csv("genre_avg_ratings.csv")
    pivot_user.to_csv("user_avg_ratings.csv")
    full_df.to_csv("cleaned_movie_ratings.csv", index=False)

    st.success("✅ Exported: movie_avg_ratings.csv, genre_avg_ratings.csv, user_avg_ratings.csv, cleaned_movie_ratings.csv")
