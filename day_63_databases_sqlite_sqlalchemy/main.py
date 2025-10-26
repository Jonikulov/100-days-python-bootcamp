"""Day 63. Databases with SQLite & SQLAlchemy"""

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Float

app = Flask(__name__)
app.config.update(
    SECRET_KEY="powerful secret key",
    # WTF_CSRF_SECRET_KEY="a csrf secret key",
    SQLALCHEMY_DATABASE_URI="sqlite:///new-books-collection.db",
)

# =============== Setting Up Database & Models ===============
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Book(db.Model):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float)

with app.app_context():
    db.create_all()

# =============== Flask Routes ===============
@app.route("/")
def home():
    result = db.session.execute(db.select(Book).order_by(Book.id))
    all_books = result.scalars().all()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Book(
            title = request.form.get("title"),
            author = request.form.get("author"),
            rating = request.form.get("rating"),
        )
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for("home"))
    return render_template("add.html")


@app.route("/edit", methods=["GET", "POST"])
def edit_rating():
    if request.method == "POST":
        book_to_update = db.get_or_404(Book, request.args.get("id"))
        book_to_update.rating = request.form["rank"]
        db.session.commit()
        return redirect(url_for("home"))

    book = db.get_or_404(Book, request.args.get("id"))
    return render_template("edit.html", book=book)


@app.route("/delete")
def delete():
    book = db.get_or_404(Book, request.args.get("id"))
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
