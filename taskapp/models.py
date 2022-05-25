from flask_login import UserMixin

from taskapp import db
from taskapp import login_manager


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    surname = db.Column(db.String(20))
    login = db.Column(db.String(25), unique=True)
    psw = db.Column(db.String(25))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
