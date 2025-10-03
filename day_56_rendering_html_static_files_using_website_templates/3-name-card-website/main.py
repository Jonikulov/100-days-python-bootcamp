"""Day 56. Rendering HTML/Static Files, Using Website Templates"""

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index_page():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
