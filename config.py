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


