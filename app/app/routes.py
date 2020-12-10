
import flask

# import forms
import models
import controllers
from helper import get_modules, string_encrypt, string_decrypt, get_id, put_id


flask.string_encrypt = string_encrypt
flask.string_decrypt = string_decrypt
flask.get_id = get_id
flask.put_id = put_id


def activate(policy):
    def wrap(f):
        def inner(*args, **kwargs):

            for rule in policy:

                if rule == 'authorized':
                    if 'user' not in flask.session:
                        return flask.redirect(flask.url_for('home'))

                if rule == 'not_authorized':
                    if 'user' in flask.session:
                        return flask.redirect(flask.url_for('home'))

            return f(_=flask,
                     method=flask.request.method,
                     form=flask.request.form,
                     querystring=flask.request.args,
                     *args, **kwargs)

        return inner
    return wrap


def init(app):

    _models = get_modules(models)
    while len(_models):
        name, model = _models.pop(0)
        for m in model.exports:
            exec(f'flask.{m.__name__} = m')
            print(f'Module loaded: {m.__name__}!')

    _controllers = get_modules(controllers)

    while len(_controllers):

        name, controller = _controllers.pop(0)

        if hasattr(controller, '__path__'):
            _controllers.extend(get_modules(controller, name))
            continue

        app.add_url_rule(
            controller.url,
            name,
            activate(controller.policy)(controller.app),
            methods=controller.methods
        )
