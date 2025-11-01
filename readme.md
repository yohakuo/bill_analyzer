## 快速使用
```
#设置一个环境变量`FLASK_APP` 来指向你的应用
$env:FLASK_APP = "microblog.py"
#运行
flask run
```

## 结构
在 Flask 中，模板以独立文件的形式编写，存储在应用程序包内的 templates 文件夹中。

## 便利性
安装python-dotenv包后，可以自动使用设定好的环境变量
flask 命令会查找 .flaskenv 文件

## 主脚本运行过程
浏览器向服务器的 / (根目录) 发起 GET 请求。
app/routes.py 里的 @app.route('/') 装饰器“捕获”了这个请求。它执行 index() 函数。
render_template() 函数启动了 Jinja2 模板引擎，读取了 app/templates/index.html 文件的内容，并将其作为“响应”(Response) 发回给浏览器。
