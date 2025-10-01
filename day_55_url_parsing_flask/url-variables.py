from flask import Flask

app = Flask(__name__)

def make_bold(func):
    def wrapper():
        return f"<b>{func()}</b>"
    return wrapper


def make_emphasis(func):
    def wrapper():
        return f"<em>{func()}</em>"
    return wrapper


def make_underlined(func):
    def wrapper():
        return f"<u>{func()}</u>"
    return wrapper


@app.route("/")
def index():
    return "<p>Index Page</p>"


@app.route("/<name>")
def greet(name):
    return f"<h1>Hello, {name}!</h1>"


@app.route("/bye")
@make_bold
@make_emphasis
@make_underlined
def say_bye():
    return "Goodbye!"


if __name__ == "__main__":
    app.run(debug=True)
