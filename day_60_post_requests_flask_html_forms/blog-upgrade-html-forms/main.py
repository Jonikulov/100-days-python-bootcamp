import os
from flask import Flask, render_template, request
import requests
from datetime import datetime
from dotenv import load_dotenv
from smtplib import SMTP

load_dotenv()
MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASS = os.getenv("GMAIL_APP_PASS")
EMAIL_PROVIDER_HOST = "smtp.gmail.com"

def send_email(name: str, email: str, phone: str | int, message: str):
    msg = "Subject: Blog Contact Form\n\n"
    msg += f"Name: {name}\n"
    msg += f"Email: {email}\n"
    msg += f"Phone: {phone}\n"
    msg += f"Message: {message}"

    with SMTP(host=EMAIL_PROVIDER_HOST) as conn:
        conn.starttls()
        conn.login(MY_EMAIL, MY_PASS)
        conn.sendmail(msg=msg, from_addr=MY_EMAIL, to_addrs=MY_EMAIL)


app = Flask(__name__)
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

@app.route("/contact", methods=["GET", "POST"])
def contact_page():
    if request.method == "POST":
        msg_sent = True
        send_email(
            request.form["name"],
            request.form["email"],
            request.form["phone"],
            request.form["message"],
        )
    else:
        msg_sent = False
    return render_template("contact.html", msg_sent=msg_sent)


if __name__ == "__main__":
    app.run(debug=True)
