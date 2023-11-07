"""routes
"""
import ast
from datetime import datetime
from urllib.parse import urlparse as url_parse

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import app, db
from app.forms import (
    ConvertForm,
    EditProfileForm,
    LoginForm,
    RegistrationForm,
    SongForm,
)
from app.models import Song, User, Video
from app.music_converter import MusicConverter
from app.video_donwloader import VideoDownloader


@app.before_request
def before_request():
    """before any request
    """
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route("/")
@app.route("/index", methods=["GET", "POST"])
@login_required
def index():
    """Root
    """
    form = SongForm()
    videos = {}
    if form.validate_on_submit():
        video = VideoDownloader(username=current_user.username)
        videos = video.search(
            interpret=form.interpret.data, title=form.title.data,
        )

    return render_template("index.html", title="Home Page", form=form, videos=videos)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login form
    """
    if current_user.is_authenticated:
        redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid User name or password")
            return redirect(url_for("login"))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")

        return redirect(next_page)

    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    """Log out user
    """
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    """register a new user
    """
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user.")

        return redirect(url_for("login"))

    return render_template("register.html", title="Register", form=form)


@app.route("/user/<username>")
@login_required
def site_user(username: str):
    """user site
    """
    user = User.query.filter_by(username=username).first_or_404()
    if user.username != current_user.username:
        return redirect(url_for("index"))
    songs = (
        Song.query
        .filter_by(user_id=user.id)
        .order_by("interpret")
        .all()
    )

    return render_template("user.html", user=user, songs=songs)


@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    """edit profile
    """
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved.")
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template(
        "edit_profile.html",
        title="Edit Profile",
        form=form,
    )


@app.route("/download/<params>")
def download(params):
    """download
    """
    user = User.query.filter_by(username=current_user.username).first()
    params = ast.literal_eval(params)
    title, interpret, video_id = tuple(params)
    title = title.replace("_", " ")
    interpret = interpret.replace("_", " ")
    video_dl = VideoDownloader(username=current_user.username)
    filename = video_dl.download_by_id(video_id=video_id)
    video = Video(
        user_id=user.id,
        video_id=video_id,
        title=title,
        interpret=interpret,
        path=filename,
        is_converted=False,
    )
    db.session.add(video)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/convert", methods=["GET", "POST"])
@login_required
def convert():
    """Convert videos to music
    """
    form = ConvertForm()
    user = User.query.filter_by(username=current_user.username).first()
    videos = Video.query.filter(
        Video.user_id == user.id,
        Video.is_converted.is_(False)
    ).all()
    if not videos:
        flash("No videos to convert")
        return redirect(url_for("index"))

    if form.validate_on_submit():
        filenames = [video.path + ".mp4" for video in videos]
        converter = MusicConverter(username=user.username)
        converter.convert(video_files=filenames)
        flash("Videos converted ...")
        for video in set(videos):
            video.set_converted()
            song = Song(
                title=video.title,
                interpret=video.interpret,
                user_id=user.id,
                url=video.video_id,
            )
            db.session.add(song)

        db.session.commit()
        flash("Database committed")

    return render_template("convert.html", title="Convert", form=form, videos=videos)
