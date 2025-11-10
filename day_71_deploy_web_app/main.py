import os
from datetime import date
from functools import wraps
from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    flash,
    abort
)
from flask_bootstrap import Bootstrap5
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user
)
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)
from sqlalchemy import Integer, String, Text, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
from gravatar import get_gravatar_url

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.getenv("WEB_APP_SECRET_KEY"),
    SQLALCHEMY_DATABASE_URI=os.getenv(
        "SQLALCHEMY_DB_URI", "sqlite:///posts.db"
    )
)
ckeditor = CKEditor(app)
Bootstrap5(app)
# Set Flask to make "gravatar" available in all templates
app.jinja_env.filters["gravatar"] = get_gravatar_url

# Setup Database
class Base(DeclarativeBase):
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}


# Connect the Database
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Configure Tables
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(String(1000), nullable=False)
    email: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    # This will act like a List of BlogPost objects attached to each User.
    # The "author" refers to the author property in the BlogPost class.
    posts: Mapped[list["BlogPost"]] = relationship(
        back_populates="post_author"
    )
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="comment_author"
    )


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    title: Mapped[str] = mapped_column(
        String(250), unique=True, nullable=False
    )
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

    # Create Foreign Key, "users.id" the users refers to the tablename of User.
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # Create reference to the User object. The "posts" refers to the posts
    # property in the User class.
    post_author: Mapped["User"] = relationship(back_populates="posts")

    comments: Mapped[list["Comment"]] = relationship(
        back_populates="parent_post"
    )


class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    comment_author: Mapped["User"] = relationship(back_populates="comments")

    post_id: Mapped[int] = mapped_column(ForeignKey("blog_posts.id"))
    parent_post: Mapped["BlogPost"] = relationship(back_populates="comments")


# Create database & tables
with app.app_context():
    db.create_all()


# Configure Flask-Login's Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(user_id):
    return db.session.get(entity=User, ident=user_id)


def admin_only(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return func(*args, **kwargs)
    return decorated_func

# ============================ Routes & Endpoints ============================

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        new_user = User(
            name = form.name.data,
            email = email,
            password = generate_password_hash(form.password.data),
        )
        user = db.session.execute(
            db.select(User).where(User.email == email)
        ).scalar_one_or_none()
        if user:
            flash("The email already registered, log in instead.")
            return redirect(url_for("login"))

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("get_all_posts"))

    if current_user.is_authenticated:
        return redirect(url_for("get_all_posts"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("The email does not exist.")
            return render_template("login.html", form=login_form)
        elif not check_password_hash(user.password, password):
            flash("The password inccorrect.")
            return render_template("login.html", form=login_form)
        login_user(user)
        return redirect(url_for("get_all_posts"))

    if current_user.is_authenticated:
        return redirect(url_for("get_all_posts"))
    return render_template("login.html", form=login_form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("get_all_posts"))


@app.route("/")
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for("login"))

        new_comment = Comment(
            text=comment_form.comment.data,
            comment_author=current_user,
            parent_post=requested_post,
        )
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for("show_post", post_id=post_id))
    comments = db.session.execute(
        db.select(Comment).where(Comment.post_id == post_id)
    ).scalars()
    return render_template(
        "post.html",
        post=requested_post,
        form=comment_form,
        comments=comments
    )


@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            post_author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.post_author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.post_author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for("get_all_posts"))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=False, port=5005)
