import os
from dotenv import load_dotenv
from datetime import date
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField

load_dotenv()
SQLALCHEMY_DB_URI = "sqlite:///posts.db"

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.getenv("RANDOM_SECRET_KEY"),
    SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DB_URI,
)
Bootstrap5(app)
ckeditor = CKEditor(app)


# Setup Database
class Base(DeclarativeBase):
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}

# Connect to Database
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Configure Table/Model
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

# Create database & tables
with app.app_context():
    db.create_all()


class CreatePostForm(FlaskForm):
    post_title = StringField("Post Title:", validators=[DataRequired()])
    subtitle = StringField("Subtitle:", validators=[DataRequired()])
    author = StringField("Author:", validators=[DataRequired()])
    img_url = StringField("Background IMG URL:", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content:", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

# ============================ Routes & Endpoints ============================
@app.route("/")
def get_all_posts():
    """Query the database for all the posts"""
    posts = db.session.execute(db.select(BlogPost)).scalars()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:post_id>")
def show_post(post_id):
    """Retrieves a BlogPost from the database based on the post_id"""
    requested_post = db.get_or_404(BlogPost, post_id)
    return render_template("post.html", post=requested_post)


@app.route("/new-post", methods=["GET", "POST"])
def add_new_post():
    """Creates a new blog post"""
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.post_title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            author=form.author.data,
            img_url=form.img_url.data,
            date=date.today().strftime("%d %B, %Y"),
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form, is_edit=False)


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id: int):
    """Updates an existing blog post"""
    post = db.get_or_404(BlogPost, post_id)
    form = CreatePostForm(
        post_title=post.title,
        subtitle=post.subtitle,
        author=post.author,
        img_url=post.img_url,
        body=post.body,
    )
    if form.validate_on_submit():
        post.title = form.post_title.data
        post.subtitle = form.subtitle.data
        post.body = form.body.data
        post.author = form.author.data
        post.img_url = form.img_url.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=form, is_edit=True)


@app.route("/delete-post/<int:post_id>")
def delete_post(post_id: int):
    """Removes a blog post from the database"""
    post_to_remove = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_remove)
    db.session.commit()
    return redirect(url_for("get_all_posts"))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
