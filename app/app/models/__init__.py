
import logging as log

import sqlalchemy.types as types
from sqlalchemy import event
from sqlalchemy import exists
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_migrate import Migrate

from helper import std_date


db = None


def init(app):
    global db

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db = SQLAlchemy(app)
    Migrate(app, db)

    @event.listens_for(Engine, "connect")
    def _set_sqlite_pragma(dbapi_connection, connection_record):
        if isinstance(dbapi_connection, SQLite3Connection):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON;")
            cursor.close()


class SaltedValue(types.TypeDecorator):
    impl = types.Unicode

    def process_bind_param(self, value, engine):
        return generate_password_hash(value)

    def process_result_value(self, value, engine):
        return value


def stringFromList(string_list):

    class StringFromList(types.TypeDecorator):
        impl = types.Unicode

        def process_bind_param(self, value, engine):

            if not value:
                return None

            if value in string_list:
                return value
            else:
                raise ValueError(f'Dude, {value} in not a valid value!')

        def process_result_value(self, value, engine):
            return value

    return StringFromList



def BooleanValue(true_value=None, false_value=None, return_orig_value=False):

    class BooleanValueClass(types.TypeDecorator):
        impl = types.Boolean

        def process_bind_param(self, value, engine):

            if true_value is None and false_value is None:
                if value:
                    return True
                else:
                    return False

            if value == true_value:
                return True
            elif value == false_value:
                return False

        def process_result_value(self, value, engine):
            if not return_orig_value or \
                    (true_value is None and false_value is None):
                return value

            if value is True:
                return true_value
            elif value is not False:
                return false_value
            else:
                return value

    return BooleanValueClass


class DateTimeString(types.TypeDecorator):
    impl = types.DateTime

    def process_bind_param(self, value, engine):

        if not value:
            return None

        if isinstance(value, str):
            return std_date(value)
        else:
            return value

    def process_result_value(self, value, engine):
        if value:
            return std_date(value)


class CRUD:

    def save(self):
        if self.id is None:
            db.session.add(self)

        try:
            return db.session.commit()
        except Exception as e:
            db.session.rollback()
            log.debug(e)

    def destroy(self):
        db.session.delete(self)

        try:
            return db.session.commit()
        except Exception as e:
            db.session.rollback()
            log.debug(e)

    def is_owner(self, session):

        try:
            return True if self.user == session['user'].get('id') else False
        except Exception as e:
            log.debug(e)
            return

    def set_owner(self, session):
        try:
            self.user = session['user'].get('id')
            return True
        except Exception as e:
            log.debug(e)

    @classmethod
    def find(cls, column, value):
        if type(column) == str:
            _column = getattr(cls, column)
        else:
            _column = column
        return db.session.query(cls).filter(_column == value)

    @classmethod
    def all(cls):
        return db.session.query(cls).all()

    @classmethod
    def like(cls, column, value):
        if not value:
            pass

        _column = getattr(cls, column)
        return db.session.query(cls).filter(_column.like(f'%{value}%'))

    @classmethod
    def exists(cls, condition):
        try:
            return db.session.query(exists().where(condition)).scalar()
        except Exception as e:
            log.debug(e)

    @classmethod
    def last(cls, session=None):
        try:
            if session:
                return db.session.query(cls).filter(
                    cls.user == session['user'].get('id')
                ).order_by(cls.id.desc()).first()

            return db.session.query(cls).order_by(cls.id.desc()).first()
        except Exception as e:
            log.debug(e)

    @classmethod
    def by_user(cls, session):
        try:
            return cls.query.filter(cls.user == session['user'].get('id'))
        except Exception as e:
            log.debug(e)

    @classmethod
    def create_by_form(cls, form, *args):
        _form = {}
        for arg in args:
            key = arg.name
            if key in form:
                _form[key] = form[key]

        return cls(**_form)
