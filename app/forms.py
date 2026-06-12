"""WTForms definitions with server-side validation.

Every user-supplied value is validated here before it ever reaches the
database, replacing the original script's complete lack of validation.
CSRF protection is provided automatically by Flask-WTF.
"""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import (
    DateTimeLocalField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    NumberRange,
    Regexp,
    ValidationError,
)

from .models import SEAT_CLASSES, User

PHONE_REGEX = r"^\+?[0-9\s\-]{7,15}$"
USERNAME_REGEX = r"^[A-Za-z0-9_.-]+$"


class SignupForm(FlaskForm):
    first_name = StringField("First name", validators=[DataRequired(), Length(max=64)])
    last_name = StringField("Last name", validators=[DataRequired(), Length(max=64)])
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=64),
            Regexp(USERNAME_REGEX, message="Letters, numbers, . _ - only."),
        ],
    )
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    phone = StringField(
        "Phone",
        validators=[
            DataRequired(),
            Regexp(PHONE_REGEX, message="Enter a valid phone number."),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, message="Use at least 8 characters."),
        ],
    )
    confirm = PasswordField(
        "Confirm password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    submit = SubmitField("Create account")

    def validate_username(self, field) -> None:  # noqa: ANN001
        if User.query.filter_by(username=field.data.strip()).first():
            raise ValidationError("That username is already taken.")

    def validate_email(self, field) -> None:  # noqa: ANN001
        if User.query.filter_by(email=field.data.strip().lower()).first():
            raise ValidationError("An account with that email already exists.")


class LoginForm(FlaskForm):
    identifier = StringField(
        "Username or email", validators=[DataRequired(), Length(max=120)]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign in")


class BookingForm(FlaskForm):
    movie_name = StringField("Movie", validators=[DataRequired(), Length(max=120)])
    seat_class = SelectField(
        "Seat class",
        choices=[(c, c) for c in SEAT_CLASSES],
        validators=[DataRequired()],
    )
    seats = IntegerField(
        "Number of seats",
        validators=[DataRequired(), NumberRange(min=1, max=20)],
    )
    show_time = DateTimeLocalField(
        "Show time", format="%Y-%m-%dT%H:%M", validators=[DataRequired()]
    )
    snacks = TextAreaField("Snacks (optional)", validators=[Length(max=200)])
    submit = SubmitField("Confirm booking")
