
url = '/logout'
methods = ['GET']
policy = ['authorized']


def app(_, form, querystring, *args, **kwargs):

    if 'user' in _.session:
        _.session.pop('user')
        return _.redirect(_.url_for('home'))
