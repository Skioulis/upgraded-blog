import os
from flask import Flask, render_template, request
import requests
from post import Post
from dotenv import load_dotenv
import smtplib

load_dotenv("env/.env")
mail_password = os.getenv("mail_password")
mail_from=os.getenv("email_from")
mail_to=os.getenv("email_to")


app = Flask(__name__)

all_posts_url = "https://api.npoint.io/c790b4d5cab58020d391"
all_posts = requests.get(all_posts_url).json()
post_objects = []

for post in all_posts:
    post_obj = Post(post["id"], post["title"], post["subtitle"], post["body"])
    post_objects.append(post_obj)

@app.route('/')
def home():

    return render_template("index.html", posts=post_objects)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        print(data["name"])
        print(data["email"])
        print(data["phone"])
        print(data["message"])
        send_email(data["name"],data["email"],data["phone"],data["message"])

        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)



@app.route('/blog/<int:id>')
def get_post(id):
    to_post = None
    for blog_post in all_posts:
        if blog_post['id']== id:
            to_post = blog_post

    return render_template("post.html", post=to_post)


def send_email(name,email,phone,message):
    email_message=f"Subject: contact {name} \n\nfrom:{name} \nemail:{email} \nphone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=mail_from,password=mail_password)
        connection.sendmail(mail_from,mail_to,email_message)


if __name__ == "__main__":
    app.run(debug=True)