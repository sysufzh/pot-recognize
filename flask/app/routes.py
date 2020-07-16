from app import app
#从app模块中即从__init__.py中导入创建的app应用
from flask import render_template
#导入模板模块
from app.form import LoginForm


@app.route('/')
@app.route('/index')
#建立路由，通过路由可以执行其覆盖的方法，可以多个路由指向同一个方法。
def index():
    user = {'username':'duke'}
    posts = [
        {
            'author':{'username':'刘'},
            'body':'这是模板模块中的循环例子~1'
        },
        {
            'author':{'username':'忠强'},
            'body':'这是模板模块中的循环例子~2'
        }

    ]
    #将数据传递给模板
    return render_template('index.html',title = '我的', user=user, posts = posts)

@app.route('/login')
def login():
    #创建一个表单实例
    form = LoginForm()
    return render_template('login.html', title = '登录', form = form)