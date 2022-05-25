from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.secret_key = 'gdlkfhglkdhfglkdh'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///taskdb.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from taskapp import models, routes

db.create_all()

