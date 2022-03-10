from flask import render_template, request, redirect,url_for,flash
from flask_wtf import FlaskForm
from flask_login import logout_user, login_required, login_user, current_user
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, ValidationError
from App.extension import login_manager, db
from . import routes
from ..model.UserDB import User
#



@routes.route("/login", methods=['GET', 'POST'])
def login():
    '''
    For Login
    '''

    if current_user.is_authenticated:
        return redirect(url_for("routes.index"))

    form = LoginForm()
    # Validate login attempt
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.validate_password(password=form.password.data):
            login_user(user)
            return redirect(url_for("routes.index"))
        flash("Invalid username/password combination")
        return redirect(url_for("routes.index"))
    return render_template("login.html", form=form)


@routes.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # print("DATA : " + str(form.username.data))

        existing_user = User.query.filter_by(username=form.username.data).first()
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_user is None and existing_email is None:
            user = User(
                username=form.username.data, email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data
            )

            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()  # Create new user
            login_user(user)  # Log in as newly created user
            return redirect(url_for("routes.index"))
        else:
            if existing_user is not None:
                flash("The username has already been taken. Please try again")

            if existing_email is not None:
                flash("The email address has already been taken. Please try again")
    return render_template("register.html", title="Register", form =form)


@login_required
@routes.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("routes.index"))


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthenticated():
    # Redirect User to home pages
    return render_template("")

#



# FORM FOR LOGIN / REGISTER
class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired()]
    )
    email = EmailField(
        'Email',
        validators=[
            DataRequired(),
            Email("Enter a valid email"),
            Length(min=6, message="email must be at least 6 characters")
        ]
    )
    first_name = StringField(
        'First Name',
        validators=[DataRequired()]
    )

    last_name = StringField('Last Name', validators=[DataRequired()])

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6, message='Select a stronger password.'),
        ]
    )
    confirm = PasswordField(
        'Confirm Your Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """User Log-in Form."""
    email = EmailField(
        "Email", validators=[DataRequired(), Email(message="Enter a valid email.")]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")