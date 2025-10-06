from flask import Flask, render_template

from post import Post

app = Flask(__name__)
posts = Post()
blog_data = posts.get_all_posts()

@app.route("/")
def home():
    return render_template("index.html", all_posts=blog_data)


@app.route("/post/<int:post_id>")
def get_post(post_id):
    return render_template("post.html", post=posts.get_post(post_id))


if __name__ == "__main__":
    app.run(debug=True)
