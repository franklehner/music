"""ORM - models
"""
from datetime import datetime
from hashlib import md5

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login


class User(UserMixin, db.Model):  # type: ignore[name-defined]
    """User
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))
    songs = db.relationship("Song", backref="author", lazy="dynamic")
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password: str):
        """set encrypted password
        """
        self.password_hash = generate_password_hash(password=password)

    def check_password(self, password: str) -> bool:
        """Check if hash decrypted is equal to password
        """
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        """Use avatar
        """
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()

        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"


class Song(db.Model):  # type: ignore[name-defined]
    """Song
    """

    __tablename__ = "songs"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(
        db.DateTime,
        index=True,
        default=datetime.utcnow,
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
    )
    interpret = db.Column(db.String(120))
    title = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False, unique=True)

    def __repr__(self):
        return f"<Song {self.title}>"


@login.user_loader
def load_user(user_id: int) -> User:
    """load user
    """
    return User.query.get(int(user_id))
