import sqlite3

db = sqlite3.connect("books-collection.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY,
    title varchar(250) NOT NULL UNIQUE,
    author varchar(250) NOT NULL,
    rating FLOAT NOT NULL
)
""")

cursor.execute("""
    INSERT INTO books (title, author, rating)
    VALUES (@title, @author, @rating)
    """,
    {
        "title": "O'tkan Kunlar",
        "author": "Abdulla Qodiriy",
        "rating": 5,
    }
)

db.commit()
cursor.close()
db.close()
