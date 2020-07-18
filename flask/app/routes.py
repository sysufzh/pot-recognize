from app import app
#从app模块中即从__init__.py中导入创建的app应用
from flask import render_template, flash, redirect, url_for,request
#导入模板模块
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm


@app.route('/')
@app.route('/index')
#建立路由，通过路由可以执行其覆盖的方法，可以多个路由指向同一个方法。
#这样，必须登录后才能访问首页了，会自动跳转到登录页
# @login_required
def index():
    # user = {'username':'duke'}
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
    #判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    #创建一个表单实例
    form = LoginForm()
    #验证表格中的数据格式是否正确
    if form.validate_on_submit():
        #根据表格里的数据进行查询，如果查询到数据返回User对象，否则返回None
        user = User.query.filter_by(username = form.usernaem.data).first()
        #判断用户不存在或密码不正确
        if user is None or not user.check_password(form.password.data):
            #如果用户不存在或者密码不正确就会闪现这条信息
            flash('无效的用户名或密码')
            #然后重定向到登录页面
            return redirect(url_for('login'))
        #这是一个非常方便的方法，当用户名和密码都正确时来解决记住用户是否记住登录状态的问题
        login_user(user,remember=form.remember_me.data)
        #此时next_page记录的是跳转至登录页面的地址
        next_page = request.args.get('next')
        #如果next_page记录的地址不存在那么就返回首页
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        #综上，登录后要么重定向至跳转的页面，要么跳转到首页
        return redirect(next_page)
    #首次登录/数据格式错误都会是在登录界面
    return render_template('login.html', title = '登录', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('恭喜你成为我们网站的新用户!')
        return redirect(url_for('login'))
    return render_template('register.html', title='注册', form=form)

@app.route('/user/<username>')
@login_required
def user(username):

    user = User.query.filter_by(username = username).first_or_404()
    posts = [
        {'author':user, 'body':'测试一号'},
        {'author':user, 'body':'测试二号'}
    ]

    return render_template('user.html', user=user, posts=posts)
    
