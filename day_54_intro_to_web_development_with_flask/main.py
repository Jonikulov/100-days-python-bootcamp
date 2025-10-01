"""Day 54. Introduction to Web Development with Flask"""

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>"

@app.route("/bye")
def say_bye():
    return "<p>Bye!</p>"


if __name__ == "__main__":
    app.run(debug=True)
