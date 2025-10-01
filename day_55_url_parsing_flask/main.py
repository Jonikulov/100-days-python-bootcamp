"""Day 55. Advanced Decorators, Rendering HTML, Parsing URLs and Flask \
Debugging, the Higher Lower Game"""

from flask import Flask
import random

app = Flask(__name__)
random_num = random.randint(0, 9)

@app.route("/")
def index_page():
    print("RANDOM NUMBER:", random_num)  # TODO: debugging
    return """<h1>Guess a number between 0 and 9</h1>
    <img src="https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif" />
    """


@app.route("/<int:num>")
def guess_number(num):
    if num > random_num:
        return """<h1 style="text-color: purple">Too High. Try Again!</h1>
        <img src="https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif" />
        """
    elif num == random_num:
        return """<h1 style="text-color: green">You Found It!</h1>
        <img src="https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif" />
        """
    return """<h1 style="text-color: red">Too Low. Try Again!</h1>
    <img src="https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif" />
    """


if __name__ == "__main__":
    app.run(debug=True)
