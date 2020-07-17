import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = 'seclaqi30984#$%(cdeFEDZQ1@'
    #格式为mysql+pymysql://数据库用户名:密码@数据库地址:端口号/数据库的名字?数据库格式
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@0.0.0.0:3306/flaskblog?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
