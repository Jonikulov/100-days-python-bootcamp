from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, desc
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
import requests
from dotenv import load_dotenv

load_dotenv()
MOVIEDB_API_READ_TOKEN = os.getenv("MOVIEDB_API_READ_TOKEN")

app = Flask(__name__)
app.config.update(
    SECRET_KEY="a powerful secret key",
    SQLALCHEMY_DATABASE_URI="sqlite:///movies.db",
)
Bootstrap5(app)

# =============== CREATE DB ===============
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

# =============== CREATE TABLE ===============
class Movie(db.Model):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(350), nullable=True)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(350), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()

class SearchMovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Search Movie")


class RateMovieForm(FlaskForm):
    ranking = StringField("Ranking", validators=[DataRequired()])
    review = StringField("Review", validators=[DataRequired()])
    submit = SubmitField("Done")


def search_movie(title: str) -> list:
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "query": title,
        "include_adult": False,
        "language": "en-US",
        "page": 1,
    }
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {MOVIEDB_API_READ_TOKEN}"
    }
    resp = requests.get(url, params=params, headers=headers)
    return resp.json()["results"]


def get_movie_details(movie_id: int | str) -> dict:
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {MOVIEDB_API_READ_TOKEN}"
    }
    resp = requests.get(url, headers=headers)
    return resp.json()

# =============== Flask Routes ===============
@app.route("/")
def home():
    result = db.session.execute(
        db.select(Movie).order_by(desc(Movie.rating), desc(Movie.ranking))
    )
    all_movies = result.scalars()
    return render_template("index.html", movies=all_movies)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = SearchMovieForm()
    if form.validate_on_submit():
        movies_list = search_movie(form.title.data)
        return render_template("select.html", movies=movies_list)
    return render_template("add.html", form=form)


@app.route("/select")
def select():
    movie_info = get_movie_details(request.args.get("movie_id"))
    img_url = "https://image.tmdb.org/t/p/w500" + movie_info.get("poster_path")
    movie = Movie(
        title=movie_info.get("title"),
        description=movie_info.get("overview"),
        year=int(movie_info.get("release_date").split("-")[0]),
        rating=f"{movie_info.get("vote_average"):.1f}",
        img_url=img_url,
    )
    db.session.add(movie)
    db.session.commit()
    return redirect(url_for("edit", id=movie.id))


@app.route("/edit", methods=["GET", "POST"])
def edit():
    form = RateMovieForm()
    movie = db.get_or_404(Movie, request.args.get("id"))
    if form.validate_on_submit():
        movie_to_update = db.get_or_404(Movie, movie.id)
        movie_to_update.ranking = float(form.ranking.data)
        movie_to_update.review = form.review.data
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("edit.html", form=form, movie=movie)


@app.route("/delete")
def delete():
    movie = db.get_or_404(Movie, request.args.get("id"))
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
