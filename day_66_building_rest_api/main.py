from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from dotenv import load_dotenv
import os
import random

load_dotenv()
SQLALCHEMY_DB_URI = f"sqlite:///{os.getenv("SQLITE_DATABASE_NAME")}"

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.getenv("RANDOM_SECRET_KEY"),
    SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DB_URI,
)

# CREATE DB
class Base(DeclarativeBase):
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}

# Connect to Database
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()

# ============================= Routes & APIs =============================
@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read a Record
@app.route("/random", methods=["GET"])
def get_random_cafe():
    cafe_id = random.choice(list(range(1, 22)))
    cafe = db.get_or_404(Cafe, cafe_id)
    return jsonify(cafe.to_dict())


# HTTP GET - Read All Record
@app.route("/all")
def get_all():
    all_cafes = db.session.execute(
        db.select(Cafe).order_by(Cafe.id)
    ).scalars()
    return jsonify([cafe.to_dict() for cafe in all_cafes])


@app.route("/search")
def search_cafe():
    cafe_loc = request.args.get("loc")
    cafes = db.session.execute(
        db.select(Cafe)
        .where(Cafe.location.contains(cafe_loc))
        .order_by(Cafe.id)
    ).scalars().all()
    if cafes:
        return jsonify([cafe.to_dict() for cafe in cafes])
    return jsonify({
        "error": {"Not Found": "Sorry, we don't have a cafe at that location."}
    }), 404


# HTTP POST - Create a Record
@app.route("/add", methods=["POST"])
def add_cafe():
    db.session.add(Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        seats=request.form.get("seats"),
        has_toilet=bool(request.form.get("has_toilet")),
        has_wifi=bool(request.form.get("has_wifi")),
        has_sockets=bool(request.form.get("has_sockets")),
        can_take_calls=bool(request.form.get("can_take_calls")),
        coffee_price=request.form.get("coffee_price"),
    ))
    db.session.commit()
    return jsonify({
        "response": {
            "success": "Successfully added the new cafe."
        }
    })


# HTTP PUT/PATCH - Update a Record
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id: int):
    cafe = db.session.execute(
        db.select(Cafe).where(Cafe.id == cafe_id)
    ).scalar()
    # cafe = db.session.get(entity=Cafe, ident=cafe_id)  # Returns None if cafe_id is not found
    if cafe:
        cafe.coffee_price = request.args.get("coffee_price")
        db.session.commit()
        return jsonify({
            "sucess": "Successfully updated the price."
        }), 200
    return jsonify({
        "error": {
            "Not Found": "Sorry a cafe with that id was not found in the database."
        }
    }), 404


# HTTP DELETE - Delete a Record
@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id: int):
    if request.args.get("api-key") != "TopSecretAPIKey":
        return jsonify({
            "error": {"Forbidden": "Invalid API key."}
        }), 403
    cafe = db.session.get(entity=Cafe, ident=cafe_id)
    if cafe:
        db.session.delete(cafe)
        db.session.commit()
        return jsonify({
            "sucess": "Sucessfully deleted the cafe."
        }), 200
    return jsonify({
        "error": {
            "Not Found": "Sorry a cafe with that id was not found in the database."
        }
    }), 404


if __name__ == "__main__":
    app.run(debug=True)
