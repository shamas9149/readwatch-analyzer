import streamlit as st
import sqlite3
import random

connection_books = sqlite3.connect("books.db")
book_cursor = connection_books.cursor()

movies_connection = sqlite3.connect("movies.db")
movies_cursor = movies_connection.cursor()

st.title("📖🎬 My Reading & Watching Dashboard")
st.divider()

# ---- BOOK STATS ----
with st.container(border=True):
    st.subheader("📚 Book Stats")

    book_cursor.execute("SELECT COUNT(*) FROM books WHERE exclusive_shelf='read'")
    count = book_cursor.fetchone()[0]

    book_cursor.execute("SELECT SUM(pages) FROM books WHERE exclusive_shelf='read'")
    count_pages = book_cursor.fetchone()[0]

    book_cursor.execute("SELECT AVG(rating) FROM books WHERE exclusive_shelf='read' AND rating != 0")
    avg_book_rating = book_cursor.fetchone()[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Books Read", count)
    col2.metric("Pages Read", count_pages)
    col3.metric("Average Rating", round(avg_book_rating, 2) if avg_book_rating else "N/A")

st.divider()

# ---- MOVIE STATS ----
with st.container(border=True):
    st.subheader("🎥 Movie Stats")

    movies_cursor.execute("SELECT COUNT(*) FROM movies WHERE special_character='Watched'")
    count_movies = movies_cursor.fetchone()[0]

    movies_cursor.execute("SELECT AVG(rating) FROM movies WHERE special_character='Watched' AND Rating != 0")
    avg_movie_rating = movies_cursor.fetchone()[0]

    col1, col2 = st.columns(2)
    col1.metric("Movies Watched", count_movies)
    col2.metric("Average Rating", round(avg_movie_rating, 2) if avg_movie_rating else "N/A")

st.divider()

# ---- RANDOM WATCHLIST PICK ----
st.subheader("🎲 Need Something to Watch?")
if st.button("Pick a random movie from watchlist"):
    movies_cursor.execute("SELECT Title FROM movies WHERE special_character='Not-Watched'")
    watchlist = movies_cursor.fetchall()
    if watchlist:
        st.success(random.choice(watchlist)[0])
    else:
        st.warning("Your watchlist is empty!")

st.divider()

# ---- 5-STAR BOOKS ----
st.subheader("🌟 5-Star Books")
book_cursor.execute("SELECT Title FROM books WHERE rating='5'")
five_star_books = book_cursor.fetchall()
st.dataframe(five_star_books, use_container_width=True)

st.divider()

# ---- 5-STAR MOVIES ----
st.subheader("🌟 5-Star Movies")
movies_cursor.execute("SELECT Title FROM movies WHERE Rating='5'")
five_star_movies = movies_cursor.fetchall()
st.dataframe(five_star_movies, use_container_width=True)