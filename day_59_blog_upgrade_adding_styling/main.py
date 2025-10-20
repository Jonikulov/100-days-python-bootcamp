from flask import Flask, render_template
import requests
from datetime import datetime

app = Flask(__name__)
# TODO: list -> dict: id, body, title, subtitle, image_url, author, dates
blog_data_url = "https://api.npoint.io/0c7a675dc18034b2da20"
blog_data = requests.get(blog_data_url).json()
for blog in blog_data:
    blog_date = datetime.strptime(blog["dates"], "%Y-%m-%d")
    blog["formatted_date"] = blog_date.strftime("%B %d, %Y")

@app.route("/")
def index_page():
    return render_template("index.html", blog_data=blog_data)

@app.route("/about")
def about_page():
    return render_template("about.html")

@app.route("/post/<int:index>")
def post_page(index):
    post_data = {}
    for post_data in blog_data:
        if post_data["id"] == index:
            break
    return render_template("post.html", post_data=post_data)

@app.route("/contact")
def contact_page():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
