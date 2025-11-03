"""Login and Registering Users with Authentication"""

import os
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    url_for,
    redirect,
    flash,
    send_from_directory
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, desc
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    current_user,
    logout_user
)

load_dotenv()
SQLALCHEMY_DB_URI = "sqlite:///users.db"

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.getenv("RANDOM_SECRET_KEY"),
    SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DB_URI,
)

# Setup Database
class Base(DeclarativeBase):
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}

# Connect the Database
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Configure Table/Model
class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(1000))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))


# Create database & tables
with app.app_context():
    db.create_all()

# Configure Flask-Login's Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))  # TODO: is user_id should be integer?
    # OR
    # return db.get_or_404(User, user_id)

# ============================ Routes & Endpoints ============================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        new_user = User(
            name = request.form.get("name"),
            email = email,
            password = generate_password_hash(request.form.get("password")),
        )
        user = db.session.execute(
            db.select(User).where(User.email == email)
        ).scalar_one_or_none()
        if user:
            flash("The email already registered, log in instead.")
            return redirect(url_for("login"))

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))

    if current_user.is_authenticated:
        return redirect(url_for("secrets"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("The email does not exist.")
            return render_template("login.html")
        elif not check_password_hash(user.password, password):
            flash("The password inccorrect.")
            return render_template("login.html")
        login_user(user)
        return redirect(url_for("secrets"))

    if current_user.is_authenticated:
        return redirect(url_for("secrets"))
    return render_template("login.html")


@app.route("/secrets")
@login_required
def secrets():
    return render_template("secrets.html", name=current_user.name)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/download")
@login_required
def download():
    return send_from_directory("static", path="files/cheat_sheet.pdf")


if __name__ == "__main__":
    app.run(debug=True)
