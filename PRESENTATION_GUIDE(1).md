# Presentation Guide — BookBloom

## 1-minute introduction
Good morning, respected sir. My project title is **Library Book Recommendation System**. The aim of this project is to help readers find books according to their interests. Users can search books, select a genre, choose a reading mood and get matching book suggestions. I developed this project using Python, Flask, SQLite, HTML, CSS and JavaScript.

## Problem statement
Readers may have difficulty choosing a suitable book from a large collection. This project provides a simple web-based system to search, filter and discover books.

## Objectives
- Make book discovery simple.
- Search by title, author or genre.
- Filter books by genre and reading mood.
- Recommend matching books using a simple rule-based method.
- Store book details and feedback in a database.

## How to demonstrate the project
1. Open the home page and explain the dashboard.
2. Search for "Harry Potter" and show the result.
3. Click a genre such as Romance or Science.
4. Open a book's details popup.
5. Use "What are you in the mood for?" to select a genre and mood, then click Recommend.
6. Submit a sample feedback entry.
7. Open the About Project page and explain the objectives and recommendation logic.

## Explain the recommendation algorithm
The project uses content-based filtering in a simple beginner-friendly form. It compares the user's selected genre and mood with each book's stored genre and mood. It shows only matching books and sorts them by rating from highest to lowest. It does not train an AI or machine-learning model.

## Likely viva questions and answers

**Q1. What is the purpose of your project?**  
A. To help users search and discover books based on genre and reading mood.

**Q2. Which programming language did you use?**  
A. Python.

**Q3. What is Flask?**  
A. Flask is a lightweight Python web framework used to build web applications.

**Q4. What is SQLite?**  
A. SQLite is a lightweight database that stores information in a local database file.

**Q5. What is a recommendation system?**  
A. It is a system that suggests items to users based on selected interests or preferences.

**Q6. How does your recommendation work?**  
A. It filters books by the selected genre and mood, then sorts matching books by rating.

**Q7. Is this a machine-learning project?**  
A. No. It is a rule-based recommendation demo. Machine learning could be added in a future version.

**Q8. What is the use of HTML and CSS?**  
A. HTML creates the page structure and CSS controls its appearance.

**Q9. What is JavaScript used for in your project?**  
A. It opens and closes the book-details popup.

**Q10. What is the future scope?**  
A. We can add login, book issue/return tracking, librarian controls, live ratings, a larger database and machine-learning recommendations.

## Be ready to explain
- `@app.route("/")` connects the home URL to the home function.
- `request.args.get()` reads search and filter values from the URL.
- SQL `SELECT` reads book records from SQLite.
- `ORDER BY rating DESC` sorts higher ratings first.
- `INSERT INTO feedback` saves a feedback entry.
