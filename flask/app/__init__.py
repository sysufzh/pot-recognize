from flask import Flask
#导入配置文件
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

#创建app应用,__name__是python预定义变量，被设置为使用本模块.
app = Flask(__name__)
#添加配置信息
app.config.from_object(Config)
#建立数据库关系
db = SQLAlchemy(app)
#绑定app和数据库，以便进行操作
migrate = Migrate(app, db)
login = LoginManager(app)
#增加登录限制
login.login_view = 'login'

from app import routes,models
