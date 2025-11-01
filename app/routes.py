import os

from flask import redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from app import app


# 首页路由
@app.route("/")
@app.route("/index")
def index():
    user = {"username": "600"}
    # post = [
    #     {"author": {"username": "陆陆"}, "body": "晚上吃什么好呢？"},
    #     {"author": {"username": "柒柒"}, "body": "不想上课T T"},
    #     {"author": {"username": "芭芭"}, "body": "想要找个天气好的地方躺躺"},
    # ]

    return render_template("index.html  ", title="首页", user=user)


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if "bill_file" not in request.files:
        return redirect(url_for("index"))

    request.files["bill_file"]
