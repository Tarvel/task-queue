from app import db, login_manager
from datetime import datetime
import uuid
from flask_login import UserMixin, current_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin ):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False, unique=True)
    tasks = db.relationship('Tasks', backref='tsk', lazy=True)



class Tasks(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    description = db.Column(db.String, nullable=False)
    deadline = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)