import os

from flask import Flask

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
# 告诉 Flask 我们的上传目录是
# 项目根目录下的 'data' 文件夹
app.config["UPLOAD_FOLDER"] = os.path.join(basedir, "..", "data")

from app import routes
