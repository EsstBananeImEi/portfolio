from flask_login import UserMixin
from app.extensions import db
from app.extensions import login_manager


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    image = db.Column(db.String(256), nullable=False, default="default.png")


@login_manager.user_loader
def load_user(user_id):
    return User.query.options(db.load_only(User.id, User.username, User.image)).get(
        int(user_id)
    )
