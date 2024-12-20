"""ORM - models."""
from datetime import datetime
from hashlib import md5

from flask_login import UserMixin

from app import db, login


class User(UserMixin, db.Model):  # type: ignore[name-defined]
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))
    songs = db.relationship("Song", backref="author", lazy="dynamic")
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.now(datetime.timezone.utc))

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password: str):
        """Set encrypted password."""
        self.password_hash = md5(password.encode("utf-8")).hexdigest()

    def check_password(self, password: str) -> bool:
        """Check if hash decrypted is equal to password."""
        return self.password_hash == md5(password.encode("utf-8")).hexdigest()

    def avatar(self, size):
        """Use avatar."""
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()

        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"


class Song(db.Model):  # type: ignore[name-defined]
    """Song."""

    __tablename__ = "songs"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(
        db.DateTime,
        index=True,
        default=datetime.now(datetime.timezone.utc),
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


class Video(db.Model):  # type: ignore[name-defined]
    """Video."""

    __tablename__ = "videos"

    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.String(32), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    interpret = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(
        db.DateTime,
        index=True,
        default=datetime.now(datetime.timezone.utc),
    )
    is_converted = db.Column(db.Boolean, default=False)
    path = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return f"<Video {self.title} Video id: {self.video_id}"

    def set_converted(self):
        """Set convertede to true."""
        self.is_converted = True


@login.user_loader
def load_user(user_id: int) -> User:
    """Load user."""
    return User.query.get(int(user_id))
