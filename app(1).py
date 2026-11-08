import sqlite3
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "library-project-demo-key"
DB_PATH = Path(__file__).with_name("library.db")

# Starter data is inserted into SQLite the first time the app runs.
STARTER_BOOKS = [
    ("The Alchemist", "Paulo Coelho", "Fiction", "Hopeful", 4.5, 1988, "A shepherd travels in search of treasure and learns about dreams and purpose.", "A thoughtful story about following your dreams."),
    ("Pride and Prejudice", "Jane Austen", "Romance", "Feel-good", 4.7, 1813, "A classic story about family, first impressions and unexpected love.", "A charming classic for readers who enjoy relationships and wit."),
    ("The Fault in Our Stars", "John Green", "Romance", "Emotional", 4.5, 2012, "Two teenagers form a meaningful connection while facing difficult circumstances.", "An emotional contemporary story."),
    ("The Notebook", "Nicholas Sparks", "Romance", "Emotional", 4.3, 1996, "A heartfelt story about lasting love and memories.", "A popular choice for readers who enjoy heartfelt stories."),
    ("The Silent Patient", "Alex Michaelides", "Thriller", "Suspenseful", 4.4, 2019, "A psychological mystery involving a woman who suddenly stops speaking.", "A page-turning mystery with unexpected turns."),
    ("Gone Girl", "Gillian Flynn", "Thriller", "Suspenseful", 4.2, 2012, "A tense mystery about a disappearance and a complicated marriage.", "For readers who enjoy twists and suspense."),
    ("Murder on the Orient Express", "Agatha Christie", "Mystery", "Suspenseful", 4.6, 1934, "Detective Hercule Poirot investigates a puzzling train mystery.", "A classic detective story."),
    ("And Then There Were None", "Agatha Christie", "Mystery", "Suspenseful", 4.7, 1939, "Ten strangers arrive on an island where a mystery unfolds.", "A famous mystery novel with clever clues."),
    ("Harry Potter and the Philosopher's Stone", "J. K. Rowling", "Fantasy", "Adventurous", 4.8, 1997, "A young boy discovers a magical world and an extraordinary destiny.", "A magical adventure for fantasy readers."),
    ("The Hobbit", "J. R. R. Tolkien", "Fantasy", "Adventurous", 4.7, 1937, "Bilbo Baggins joins an unexpected adventure beyond his home.", "A classic journey full of imagination."),
    ("A Brief History of Time", "Stephen Hawking", "Science", "Curious", 4.4, 1988, "An introduction to big questions about space and time.", "For readers curious about the universe."),
    ("Cosmos", "Carl Sagan", "Science", "Curious", 4.6, 1980, "Explore the universe and humanity's place within it.", "A fascinating science read."),
    ("Wings of Fire", "A. P. J. Abdul Kalam", "Biography", "Inspirational", 4.7, 1999, "The inspiring life story of India's scientist and former President.", "A motivating real-life journey."),
    ("I Am Malala", "Malala Yousafzai", "Biography", "Inspirational", 4.5, 2013, "The story of a young education activist and her experiences.", "An inspiring account of courage and education."),
    ("Atomic Habits", "James Clear", "Self Help", "Motivational", 4.6, 2018, "Practical ideas for building good habits through small changes.", "Useful for readers interested in personal growth."),
    ("The 7 Habits of Highly Effective People", "Stephen R. Covey", "Self Help", "Motivational", 4.4, 1989, "A guide to personal and professional effectiveness.", "A well-known personal development book."),
    ("To Kill a Mockingbird", "Harper Lee", "Fiction", "Thoughtful", 4.6, 1960, "A powerful story about fairness, empathy and growing up.", "A thoughtful literary classic."),
    ("The Little Prince", "Antoine de Saint-Exupéry", "Fiction", "Feel-good", 4.5, 1943, "A thoughtful tale about friendship, kindness and seeing with the heart.", "A short and memorable philosophical tale.")
]

GENRES = ["All", "Fiction", "Romance", "Thriller", "Mystery", "Fantasy", "Science", "Biography", "Self Help"]
MOODS = ["Any mood", "Hopeful", "Feel-good", "Emotional", "Suspenseful", "Adventurous", "Curious", "Inspirational", "Motivational", "Thoughtful"]


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialise_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                genre TEXT NOT NULL,
                mood TEXT NOT NULL,
                rating REAL NOT NULL,
                year INTEGER NOT NULL,
                description TEXT NOT NULL,
                reason TEXT NOT NULL
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                book_title TEXT NOT NULL,
                comment TEXT NOT NULL
            )
        """)
        count = connection.execute("SELECT COUNT(*) FROM books").fetchone()[0]
        if count == 0:
            connection.executemany("""
                INSERT INTO books (title, author, genre, mood, rating, year, description, reason)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, STARTER_BOOKS)


def fetch_books(search="", genre="All", mood="Any mood", sort="recommended"):
    query = "SELECT * FROM books WHERE 1=1"
    params = []

    if genre != "All":
        query += " AND genre = ?"
        params.append(genre)
    if mood != "Any mood":
        query += " AND mood = ?"
        params.append(mood)
    if search:
        query += " AND (LOWER(title) LIKE ? OR LOWER(author) LIKE ? OR LOWER(genre) LIKE ?)"
        term = f"%{search.lower()}%"
        params.extend([term, term, term])

    if sort == "rating":
        query += " ORDER BY rating DESC, title ASC"
    elif sort == "title":
        query += " ORDER BY title COLLATE NOCASE ASC"
    else:
        query += " ORDER BY rating DESC, title ASC"

    with get_connection() as connection:
        return connection.execute(query, params).fetchall()


@app.route("/")
def home():
    search = request.args.get("search", "").strip()
    genre = request.args.get("genre", "All")
    mood = request.args.get("mood", "Any mood")
    sort = request.args.get("sort", "recommended")

    if genre not in GENRES:
        genre = "All"
    if mood not in MOODS:
        mood = "Any mood"
    if sort not in ["recommended", "rating", "title"]:
        sort = "recommended"

    books = fetch_books(search, genre, mood, sort)
    with get_connection() as connection:
        top_books = connection.execute(
            "SELECT * FROM books ORDER BY rating DESC, title ASC LIMIT 4"
        ).fetchall()
        total_books = connection.execute("SELECT COUNT(*) FROM books").fetchone()[0]

    return render_template(
        "index.html", books=books, top_books=top_books,
        genres=GENRES, moods=MOODS, selected_genre=genre,
        selected_mood=mood, selected_sort=sort, search=search,
        total_books=total_books
    )


@app.route("/recommend", methods=["POST"])
def recommend():
    genre = request.form.get("genre", "All")
    mood = request.form.get("mood", "Any mood")
    if genre not in GENRES:
        genre = "All"
    if mood not in MOODS:
        mood = "Any mood"
    return redirect(url_for("home", genre=genre, mood=mood, sort="rating"))


@app.route("/feedback", methods=["POST"])
def feedback():
    student_name = request.form.get("student_name", "").strip()
    book_title = request.form.get("book_title", "").strip()
    comment = request.form.get("comment", "").strip()

    if not student_name or not book_title or not comment:
        flash("Please complete all feedback fields.", "error")
    else:
        with get_connection() as connection:
            connection.execute(
                "INSERT INTO feedback (student_name, book_title, comment) VALUES (?, ?, ?)",
                (student_name, book_title, comment)
            )
        flash("Thank you! Your feedback has been saved.", "success")
    return redirect(url_for("home"))


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    initialise_database()
    app.run(host="0.0.0.0", port=5000, debug=True)
