#!/usr/bin/env python3

import flask
from flask import Flask, request, session

try:
    import settings

except ImportError:
    import sys
    from os.path import dirname, abspath

    p = f'{abspath(dirname(__file__))}/app'
    sys.path.append(p)

    import settings


import models
import routes
import config

app = Flask(
        __name__,
        template_folder=settings.views,
        static_folder=settings.static,
        static_url_path=settings.static_url
)

config.init(app)
models.init(app)
routes.init(app)

models.db.create_all()

flask.app = app


@app.after_request
def per_request_callbacks(response):
    path = request.path
    if not path.startswith('/static/') and path not in ['/favicon.ico']:
        models.activity.Activity.create(path, session)
    return response


if __name__ == '__main__':
    app.run(port=settings.port, debug=settings.debug)
