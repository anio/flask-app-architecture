url = '/register'
methods = ['POST', 'GET']
policy = ['not_authorized']


def app(flask, method, form, querystring, *args, **kwargs):

    _form = flask.Form_Register(form)

    if method == 'GET' or not _form.validate_on_submit():
        for error in _form.errors.items():
            print(error)
        return flask.render_template('register.html', form=_form)

    if flask.User.query.filter_by(username=form.get('username')).first():
        return 'username exists'

    user = flask.User.create_by_form(
        form,
        flask.User.name,
        flask.User.username,
        flask.User.password
    )

    user.save()
    return flask.redirect(flask.url_for('login_user'))
