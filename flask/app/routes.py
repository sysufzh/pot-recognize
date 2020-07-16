from app import app
#从app模块中即从__init__.py中导入创建的app应用
from flask import render_template, flash, redirect, url_for
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

@app.route('/login', methods = ['GET', 'POST'])
def login():
    #创建一个表单实例
    form = LoginForm()
    #验证表格中的数据格式是否正确
    if form.validate_on_submit():
        #闪现的信息会出现在页面，当然在页面上要设置
        flash('用户登录的用户名是:{}, 是否记住我:{}'.format(
            form.username.data, form.remember_me.data))
        #重新定向至首页
        return redirect(url_for('index'))
    #首次登录/数据格式错误都会是在登录界面
    return render_template('login.html', title = '登录', form = form)