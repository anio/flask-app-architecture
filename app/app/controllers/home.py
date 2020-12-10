url = '/'
methods = ['GET']
policy = []


def app(_, method, form, querystring):

    if 'user' in _.session:
        view_name = 'home.html'
    else:
        view_name = 'anon_home.html'
    return _.render_template(view_name, title="Home")
