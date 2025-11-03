import os
import traceback

from flask import redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from app import app
from src.ai_helper import get_ai_suggestion
from src.analysis import process_and_analyze_data


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


# 文件上传路由
@app.route("/upload", methods=["POST"])
def upload_file():
    if "bill_file" not in request.files:
        return redirect(url_for("index"))

    file = request.files["bill_file"]

    if file.filename == "":
        return redirect(url_for("index"))

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)
        print(f"文件 {filename} 保存到{file_path}")

        try:
            analysis_report = process_and_analyze_data(file_path)
            if analysis_report is None:
                print("[routes.py] 分析失败: process_and_analyze_data 返回了 None")
                return "分析失败，可能是文件格式不受支持或'时间'列无法解析。"

            suggestion = get_ai_suggestion(analysis_report)

            return f"""
            <h1>账单分析完成！</h1>
            <h2>AI 理财顾问的建议：</h2>
            <p>{suggestion.replace("\\n", "<br>")}</p>
            <br>
            <a href="/">返回上传新文件</a>
            """

        except Exception as e:
            print(f"[routes.py] 分析失败: {e}")
            traceback.print_exc()
            return "分析失败，请检查您的账单文件格式或联系管理员。"

    return redirect(url_for("index"))
