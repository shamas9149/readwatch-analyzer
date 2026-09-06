import csv
import sqlite3
import random
import requests
from datetime import datetime
import time


# BOOK DB
connection_books = sqlite3.connect("books.db")
book_cursor = connection_books.cursor()
book_cursor.execute("""
    CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY,
        Title VARCHAR(255),
        author VARCHAR(255),
        rating REAL,
        pages INTEGER,
        exclusive_shelf VARCHAR(50),
        cover_url VARCHAR(255)
        )
        """)
connection_books.commit()


# MOVIE DB
movies_connection = sqlite3.connect("movies.db")
movies_cursor = movies_connection.cursor()

movies_cursor.execute("""
    CREATE TABLE IF NOT EXISTS movies(
        id INTEGER PRIMARY KEY,
        Title VARCHAR(255),
        Rating REAL,
        year INTEGER,
        when_watched VARCHAR(20),
        special_character VARCHAR(255)
    )
""")
movies_connection.commit()




def get_book_data(name):
    params = {"q": name}
    
    try:
        response = requests.get("https://openlibrary.org/search.json", params=params, timeout=20)
        if response.status_code==200:
            book_data=response.json()
            if book_data["docs"]:
                first_book=book_data["docs"][0]
                return first_book
        else:
            print( f" Failed to retrive {response.status_code}")
            return None
        
    except requests.exceptions.RequestException as e:
        print("Could not connect to Open Library.")
        print(e)
        return None

# book csv to db
book_cursor.execute("SELECT COUNT(*) FROM books")
count = book_cursor.fetchall()[0][0]

if count == 0:
    with open("Goodread.csv", mode="r", newline="", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            Title = row["Title"]
            Author = row["Author"]
            rating = float(row["My Rating"])
            pages = row["Number of Pages"]
            if pages != "":
                pages = int(pages)
            else:
                pages = 0
            exclusive_shelf = row["Exclusive Shelf"]
            book_info=get_book_data(Title)
            time.sleep(0.5)
            if book_info:
                cover_i=book_info.get("cover_i")
                if cover_i:
                    cover_url=f"https://covers.openlibrary.org/b/id/{cover_i}-M.jpg"
                else:
                    cover_url=None
            else:
                cover_url=None

            sql = "INSERT INTO books(Title,author,rating,pages,exclusive_shelf,cover_url) VALUES (?,?,?,?,?,?)"
            val = (Title, Author, rating, pages, exclusive_shelf,cover_url)
            book_cursor.execute(sql, val)
    connection_books.commit()


# Letterboxd csv to db 
movies_cursor.execute("SELECT COUNT(*) FROM movies")
movie_count = movies_cursor.fetchall()[0][0]

if movie_count == 0:
    with open("letterboxd-shamashaq-2026-09-02-16-47-utc/watched.csv", mode="r", newline="", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            Title = row["Name"]
            Year = row["Year"]
            when_watched = row["Date"]
            special_character = "Watched"
            sql = "INSERT INTO movies (Title,Year,special_character,when_watched) VALUES (?,?,?,?)"
            val = (Title, Year, special_character, when_watched)
            movies_cursor.execute(sql, val)
    movies_connection.commit()

    with open("letterboxd-shamashaq-2026-09-02-16-47-utc/watchlist.csv", mode="r", newline="", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            Title = row["Name"]
            Year = row["Year"]
            special_character = "Not-Watched"
            sql = "INSERT INTO movies (Title,Year,special_character) VALUES (?,?,?)"
            val = (Title, Year, special_character)
            movies_cursor.execute(sql, val)
    movies_connection.commit()

    with open("letterboxd-shamashaq-2026-09-02-16-47-utc/ratings.csv", mode="r", newline="", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            Rating = float(row["Rating"])
            Title = row["Name"]
            sql = "UPDATE movies SET Rating=? WHERE Title = ? AND special_character='Watched'"
            val = (Rating, Title)
            movies_cursor.execute(sql, val)
    movies_connection.commit()



# Menu
if __name__ == "__main__":
    while True:
        print("1. Goodreads: ")
        print("2. Letterbox: ")
        print("3. Quit")
        choice = input("Choose an option: ")

        if choice == "1":
            while True:
                print("1. Books Read Count")
                print("2. Average Rating")
                print("3. Total Pages Read")
                print("4. 5-Star Books")
                print("5 Check when The book was first published")
                print("6. Back")
                choice = input("Choose an option: ")

                if choice == "1":
                    count = 0
                    book_cursor.execute("SELECT Title FROM books WHERE exclusive_shelf='read'")
                    my_results = book_cursor.fetchall()
                    for x in my_results:
                        count += 1
                    print("Books read: ", count)

                elif choice == "2":
                    book_cursor.execute("SELECT AVG(rating) FROM books WHERE exclusive_shelf='read' AND rating != 0")
                    my_results = book_cursor.fetchall()
                    average = my_results[0][0]
                    print("Average Rating:", round(average, 2))

                elif choice == "3":
                    pages = 0
                    book_cursor.execute("SELECT pages FROM books WHERE exclusive_shelf='read'")
                    my_results = book_cursor.fetchall()
                    for x in my_results:
                        pages += x[0]
                    print("Pages: ", pages)

                elif choice == "4":
                    book_cursor.execute("SELECT Title FROM books WHERE rating='5'")
                    my_results = book_cursor.fetchall()
                    for x in my_results:
                        print(x[0])

                elif choice == "5":
                    Title=input("Enter the book Title")
                    book_info= get_book_data(Title)

                    if book_info:
                        published= book_info.get("first_publish_year")
                        print("First published:" ,published)
                    else:
                        print("Could not find that book")   
                elif choice == "6":
                    break

        elif choice == "2":
            while True:
                print("1. Movies Watched Count")
                print("2. Pick a Random Movie from Watchlist")
                print("3. 5 star movies")
                print("4. Most movies Watched in A month")
                print("5. Longest Gap Without Watching anything")
                print("6. Lowest Rated Movies")
                print("7. Movies Watched by Year")
                print("8. Back")

                choice = input("Choose an option: ")

                if choice == "1":
                    movies_cursor.execute("SELECT COUNT(*) FROM movies WHERE special_character='Watched'")
                    Count = movies_cursor.fetchone()[0]
                    print("Movies Watched: ", Count)

                elif choice == "2":
                    movies_cursor.execute("SELECT Title FROM movies WHERE special_character='Not-Watched'")
                    my_results = movies_cursor.fetchall()
                    print(random.choice(my_results)[0])

                elif choice == "3":
                    movies_cursor.execute("SELECT Title FROM movies WHERE Rating = 5")
                    my_results = movies_cursor.fetchall()
                    for x in my_results:
                        print(x[0])

                elif choice == '4':
                    movies_cursor.execute("""
                        SELECT strftime('%Y-%m', when_watched) AS month, COUNT(*) as total
                        FROM movies
                        WHERE special_character='Watched'
                        GROUP BY month
                        ORDER BY total DESC
                        LIMIT 1
                    """)
                    my_results = movies_cursor.fetchall()
                    print(my_results[0][0], "-", my_results[0][1], "movies")

                elif choice == "5":
                    movies_cursor.execute("SELECT when_watched FROM movies WHERE special_character='Watched' ORDER BY when_watched")
                    my_results = movies_cursor.fetchall()

                    dates = []
                    for x in my_results:
                        dates.append(datetime.strptime(x[0], "%Y-%m-%d"))

                    longest_gap = 0
                    for i in range(len(dates) - 1):
                        gap = (dates[i + 1] - dates[i]).days
                        if gap > longest_gap:
                            longest_gap = gap

                    print("Longest gap without watching:", longest_gap, "days")

                elif choice == "6":
                    movies_cursor.execute("SELECT Title FROM movies WHERE Rating <= 2 ORDER BY Rating ASC LIMIT 5")
                    my_results = movies_cursor.fetchall()
                    for x in my_results:
                        print(x[0])

                elif choice == "7":
                    movies_cursor.execute("""
                        SELECT strftime('%Y', when_watched) AS watch_year, COUNT(*) as cnt
                        FROM movies
                        WHERE special_character='Watched'
                        GROUP BY watch_year
                        ORDER BY watch_year
                    """)
                    my_results = movies_cursor.fetchall()
                    for x in my_results:
                        print(x[0], "-", x[1], "movies")

                elif choice == "8":
                    break

        elif choice == "3":
            break