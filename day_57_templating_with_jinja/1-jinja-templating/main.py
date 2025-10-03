"""Day 57. URL Building & Templating with Jinja in Flask Applications"""

import random
import requests
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)
app.jinja_env.add_extension("jinja2.ext.loopcontrols")

@app.route("/")
def index_page():
    num = random.randint(1, 99)
    year = datetime.now().year
    return render_template(
        "index.html",
        rnum=num,
        current_year=year
    )


@app.route("/hello/")
@app.route("/hello/<string:name>")
def say_hello(name=None):
    return render_template("hello.html", name=name)


@app.route("/guess/<string:name>")
def guess_gender_age(name):
    resp = requests.get(f"https://api.genderize.io?name={name}")
    gender = resp.json()["gender"]
    resp = requests.get(f"https://api.agify.io?name={name}")
    age = resp.json()["age"]
    return render_template(
        "guess-gender-age.html",
        name=name.title(),
        gender=gender,
        age=age,
    )


@app.route("/blog")
def blog_website():
    resp = requests.get("https://api.npoint.io/c790b4d5cab58020d391")
    blog_data = resp.json()
    return render_template("blog.html", blog_data=blog_data)


if __name__ == "__main__":
    app.run(debug=True)
