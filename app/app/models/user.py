
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms import validators, StringField, PasswordField, SubmitField

from helper import get_current
from models import db, CRUD, SaltedValue


name = StringField(u'Name', [validators.InputRequired(),
                            validators.Length(min=3, max=32)],
                   render_kw={'placeholder': u'Name'}
                   )
username = StringField(u'Username', [validators.InputRequired(),
                                       validators.Length(min=3, max=32)],

                   render_kw={'placeholder': u'Username'}
                       )
password = PasswordField(u'Passowrd', [validators.InputRequired(),
                                        validators.Length(min=8, max=128)],

                   render_kw={'placeholder': u'Password'}
                         )


class User(db.Model, CRUD):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.UnicodeText)
    email = db.Column(db.UnicodeText, unique=True)
    username = db.Column(db.UnicodeText, unique=True, nullable=False)
    password = db.Column(SaltedValue, nullable=False)
    role = db.Column(db.Integer, default=1000, nullable=False)

    created_date = db.Column(db.DateTime, default=get_current)

    def is_valid_passowrd(self, password):
        return check_password_hash(self.password, password)


class Form_Register(FlaskForm):
    name = name
    username = username
    password = password
    submit = SubmitField('Signup')


class Form_Login(FlaskForm):
    username = username
    password = password
    submit = SubmitField('Login')


exports = (User, Form_Register, Form_Login)
