from flask_login import UserMixin

from App.extension import db
from geoalchemy2 import Geometry
from App.settings.config import Config
from werkzeug.security import generate_password_hash, check_password_hash


# For Account
# UserMixin has is_authenticated
class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    username = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )
    first_name = db.Column(
        db.String(100),
        nullable=False,
        unique=False
    )
    last_name = db.Column(
        db.String(100),
        nullable=False,
        unique=False
    )
    email = db.Column(
        db.String(150),
        nullable=False,
        unique=False
    )
    password = db.Column(
        db.String(255),
        nullable=False
    )
    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True,
        default=db.func.current_timestamp()
    )
    last_login = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )

    admin = db.Column(
        db.Boolean,
        unique=False,
        default=False
    )
    driver = db.Column(
        db.Boolean,
        unique=False,
        default=False
    )
    customer = db.Column(
        db.Boolean,
        unique=False,
        default=True
    )

    def set_password(self, password):
        self.password = generate_password_hash(
            password,
            method='sha256',
        )

    def validate_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.username
