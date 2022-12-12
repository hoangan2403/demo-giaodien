from urllib.parse import quote
from flask import Flask
from  urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/hotelappdb?charset=utf8mb4' % quote('12345678')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


db = SQLAlchemy(app=app)