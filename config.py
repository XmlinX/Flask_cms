import os
from datetime import timedelta

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'bbs'
USERNAME = 'root'
PASSWORD = 'root'


DB_URI = 'mysql+pymysql://{username}:{password}@{hostname}:{port}/{database}'.format(username=USERNAME, password=PASSWORD, hostname=HOSTNAME, port=PORT, database=DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False # 如果设置为True，会经常发送模型变更通知

PERMANENT_SESSION_LIFETIME = timedelta(hours=5)

DEBUG = True

CmsUid = 'cms_login'

SECRET_KEY = os.urandom(24)


# 邮件发送配置
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = '465'
# MAIL_USE_TLS = False
MAIL_USE_SSL = True
# MAIL_DEBUG : default app.debug
MAIL_USERNAME = '547816252@qq.com'
MAIL_PASSWORD = 'wrhrruhrcwigbcae'
MAIL_DEFAULT_SENDER = '547816252@qq.com'
# MAIL_MAX_EMAILS : default None
# MAIL_SUPPRESS_SEND : default app.testing
# MAIL_ASCII_ATTACHMENTS : default False


# MAIL_USE_TLS：端口号587
# MAIL_USE_SSL：端口号465
# QQ邮箱不支持非加密方式发送邮件