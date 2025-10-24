from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config["SECRET_KEY"] = "7a69b44e468847ca94d7283d1a08b9e7"
Bootstrap5(app)

class CafeForm(FlaskForm):
    cafe = StringField(
        "Cafe name",
        validators=[DataRequired()]
    )
    location_url = StringField(
        "Cafe Location on Google Maps (URL)",
        validators=[DataRequired(), URL()]
    )
    open_time = StringField(
        "Opening Time e.g. 8AM",
        validators=[DataRequired()]
    )
    closing_time = StringField(
        "Closing Time e.g. 5:30PM",
        validators=[DataRequired()]
    )
    coffee_rating = SelectField(
        "Coffee Rating",
        choices=["☕️" * i for i in range(1, 6)],
        validators=[DataRequired()]
    )
    wifi_rating = SelectField(
        "Wifi Strength Rating",
        choices=["✘"] + ["💪" * i for i in range(1, 6)],
        validators=[DataRequired()]
    )
    power_rating = SelectField(
        "Power Socket Availability",
        choices=["✘"] + ["🔌" * i for i in range(1, 6)],
        validators=[DataRequired()]
    )
    submit = SubmitField("Submit", render_kw={"class": "btn-light"})


# All Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        # Write a new row into cafe-data.csv
        with open("cafe-data.csv", mode="a", encoding="utf-8") as file:
            file.write(
                f"\n{form.cafe.data},"
                f"{form.location_url.data},"
                f"{form.open_time.data},"
                f"{form.closing_time.data},"
                f"{form.coffee_rating.data},"
                f"{form.wifi_rating.data},"
                f"{form.power_rating.data}"
            )
        return redirect(url_for('cafes'))
    return render_template("add.html", form=form)


@app.route("/cafes")
def cafes():
    with open("cafe-data.csv", newline="", encoding="utf-8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=",")
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template("cafes.html", cafes=list_of_rows)


if __name__ == "__main__":
    app.run(debug=True)
