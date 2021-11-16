url = '/'
methods = ['GET']
policy = []


def app(flask, method, form, querystring):

    if 'user' in flask.session:
        view_name = 'home.html'
    else:
        view_name = 'anon_home.html'
    return flask.render_template(view_name, title="Home")
