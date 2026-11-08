# BookBloom — Library Book Recommendation System

A presentation-ready college Project-Based Learning (PBL) project built with Python, Flask, SQLite, HTML, CSS and JavaScript.

## Main features
1. Search books by title, author or genre.
2. Browse books by category.
3. Filter books by reading mood.
4. Recommend matching books and sort them by sample rating.
5. View detailed book information in a popup.
6. Display top-rated sample books.
7. Save user feedback in an SQLite database.
8. Responsive layout for mobile and desktop.
9. Separate About Project page explaining the problem, objectives and method.

## Technology stack
- Python 3 — application logic
- Flask — web framework and URL routing
- SQLite — stores book records and feedback
- HTML — page structure
- CSS — responsive design
- JavaScript — book details popup
- Jinja2 — dynamic HTML templates

## Folder structure
```text
Library-Book-Recommendation-System/
├── app.py
├── requirements.txt
├── README.md
├── PRESENTATION_GUIDE.md
├── templates/
│   ├── index.html
│   └── about.html
└── static/
    ├── style.css
    └── script.js
```

## Run on Replit
1. Create a Python Repl.
2. Upload the files and folders while keeping the same folder structure.
3. In the Shell, run: `pip install -r requirements.txt`
4. Run: `python app.py`
5. Open the Webview preview.

The `library.db` database is created automatically when the app starts for the first time.

## Run on a computer
```bash
pip install -r requirements.txt
python app.py
```
Open `http://127.0.0.1:5000` in your browser.

## Recommendation logic
This is a simple content-filtering recommendation system:
- The user selects a preferred genre and/or reading mood.
- The program filters database records that match the selected options.
- Matching books are sorted by their sample rating in descending order.
- The matching list is displayed to the user.

This is a rule-based educational recommendation demo, not a machine-learning model.

## Database
SQLite creates two tables:
- `books`: title, author, genre, mood, rating, year and descriptions.
- `feedback`: student name, book title and feedback comment.

## Important note
The book catalogue and ratings are sample data for demonstration. Ratings are illustrative and are not live user reviews. Add more entries to `STARTER_BOOKS` in `app.py` to expand the catalogue.
