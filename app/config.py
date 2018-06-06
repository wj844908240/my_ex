# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import datetime
from flask_jwt_extended import JWTManager
from elasticsearch_dsl.connections import connections
app = Flask(__name__)
CORS(app)

# 内网服务器mysql地址
localConfig = 'mysql+pymysql://root:123456@192.168.5.114:3306/zzh'

app.config['SQLALCHEMY_DATABASE_URI'] = localConfig
# 开启数据库查询性能测试
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config[
    'SECRET_KEY'] = '\x88D\xf09\x91\x07\x98\x89\x87\x96\xa0A\xc68\xf9\xecJ:U\x17\xc5V\xbe\x8b\xef\xd7\xd8\xd3\xe6\x98*4'

db = SQLAlchemy(app)

# app config
# delta = datetime.timedelta(minutes=2)
delta = datetime.timedelta(hours=6)
refresh_delta = datetime.timedelta(days=30)
# add by tyf 2017-7-31
app.config['JWT_IDENTITY_CLAIM'] = "identity"
app.config['JWT_TOKEN_LOCATION'] = ["headers"]
app.config['JWT_HEADER_NAME'] = "zzhToken"
app.config['JWT_HEADER_TYPE'] = "Basic"
app.config['JWT_AUTH_URL_RULE'] = "/login"
app.config['JWT_ALGORITHM'] = "HS256"
app.config['JWT_SECRET_KEY'] = "aaa"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = delta
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = refresh_delta
jwt = JWTManager(app)


SECRET_KEY = "my blog"

# Elasticsearch新建连接
connections.create_connection(hosts="192.168.5.114:9200")