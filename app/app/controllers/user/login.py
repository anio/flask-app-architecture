url = '/login'
methods = ['POST', 'GET']
policy = ['not_authorized']


def app(flask, method, form, querystring, *args, **kwargs):

    _form = flask.Form_Login(form)

    if method == 'GET' or not _form.validate_on_submit():
        for error in _form.errors.items():
            print(error)
        return flask.render_template('login.html', form=_form)

    username = form.get('username', None)
    password = form.get('password', None)

    if not all([username, password]):
        return flask.redirect(flask.url_for('login_user'))

    user = flask.User.query.filter_by(username=username).first()

    if user and user.is_valid_passowrd(password):

        flask.session['user'] = {
            'id': user.id,
            'username': user.username,
            'name': user.name
        }

        return flask.redirect(flask.url_for('home'))
    else:
        return flask.redirect(flask.url_for('login_user'))
