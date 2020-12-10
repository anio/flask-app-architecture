
import flask

import helper


def init(app):

    app.config['SECRET_KEY'] = 'set-me-please'

    @app.context_processor
    def inject_to_templates():
        return dict(
            _=flask,
            session=flask.session,
            user=flask.session.get('user', None),
            helper=helper,
        )
