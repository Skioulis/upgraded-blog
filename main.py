from flask import Flask, render_template
import requests
from post import Post


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

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/blog/<int:id>')
def get_post(id):
    to_post = None
    for blog_post in all_posts:
        if blog_post['id']== id:
            to_post = blog_post

    return render_template("post.html", post=to_post)

if __name__ == "__main__":
    app.run(debug=True)