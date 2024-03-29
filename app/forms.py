"""Forms
"""
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    ValidationError,
)

from app.models import User


class LoginForm(FlaskForm):
    """Login form
    """
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign in")


class RegistrationForm(FlaskForm):
    """Registration form
    """
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password",
        validators=[DataRequired(), EqualTo("password")],
    )
    submit = SubmitField("Register")

    def validate_username(self, username: StringField):
        """validate username
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email: StringField):
        """Check that emails are unique
        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address")


class EditProfileForm(FlaskForm):
    """EditProfileForm
    """
    username = StringField("Username", validators=[DataRequired()])
    about_me = TextAreaField("About me", validators=[Length(min=0, max=140)])
    submit = SubmitField("Submit")


class SongForm(FlaskForm):
    """Song form
    """
    interpret = StringField("Interpret")
    title = StringField("Titel")
    search = SubmitField("Search")
    download = SubmitField("download")

class ConvertForm(FlaskForm):
    """Convert Form
    """
    submit = SubmitField("Submit")
