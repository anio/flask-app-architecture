
# A Better Architecture For Flask-based Application

This is a Flask application with a better approach and design, and more pythonic code style.
You can use it as a boilerplate code, but it's just a proof-of-concept code.

## Easy to write controllers

Just add your controller to the `controllers` directory and define:

* `app` function
* `url`
* http `methods`
* access control `policy`

and use:
* `_.ModelName`, `_.string_encrypt`, `_.string_decrypt`
* `form` instead of `from flask import request` and `request.from`
* `querystring` instead of `request.args`

```Python
url = '/register'
methods = ['POST', 'GET']
policy = ['not_authorized']


def app(_, method, form, querystring, *args, **kwargs):

    _form = _.Form_Register(form)

    if method == 'GET' or not _form.validate_on_submit():
        for error in _form.errors.items():
            print(error)
        return _.render_template('register.html', form=_form)

    user = _.User.create_by_form(
        form,
        _.User.name,
        _.User.username,
        _.User.password
    )

    user.save()
    return _.redirect(_.url_for('login_user'))
```

[Read the routes code](app/app/routes.py)

## Easy to write models and form

```Python

from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms import validators, StringField, PasswordField, SubmitField

from helper import get_current
from models import db, CRUD, SaltedValue


name = StringField(u'Name', [validators.InputRequired(), validators.Length(min=3, max=32)])
username = StringField(u'Username', [validators.InputRequired(), validators.Length(min=3, max=32)])
password = PasswordField(u'Passowrd', [validators.InputRequired(), validators.Length(min=8, max=128)])


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

```

[Read the models \__init__ code](app/app/models/__init__.py#L119)
