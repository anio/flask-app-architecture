
url = '/logout'
methods = ['GET']
policy = ['authorized']


def app(flask, form, querystring, *args, **kwargs):

    if 'user' in flask.session:
        flask.session.pop('user')
        return flask.redirect(flask.url_for('home'))
