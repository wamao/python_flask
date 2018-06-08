# -- coding: utf-8 --

import os

DEBUG = True

SECRET_KEY = os.urandom(24)

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/test'

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = '1q89s02zbh3dh48s52h2pl5mh2'
UPLOAD_FOLDER = 'C:/Users/jimmyf123/Desktop/python/uploadfile'  #文件上传路径
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg']) #允许的文件上传格式
MAX_CONTENT_LENGTH=10 * 1024 * 1024   #允许的文件上传大小