"""routes
"""
from datetime import datetime
from urllib.parse import urlparse as url_parse

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import app, db
from app.forms import EditProfileForm, LoginForm, RegistrationForm
from app.models import Song, User


@app.before_request
def before_request():
    """before any request
    """
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route("/")
@app.route("/index")
@login_required
def index():
    """Root
    """
    posts = [
        {
            "author": {"username": "John"},
            "body": "Beautiful day in Portland",
        },
        {
            "author": {"username": "Susan"},
            "body": "The Avengers movie was so cool",
        },
    ]

    return render_template("index.html", title="Home Page", posts=posts)


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
