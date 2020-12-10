url = '/login'
methods = ['POST', 'GET']
policy = ['not_authorized']


def app(_, method, form, querystring, *args, **kwargs):

    _form = _.Form_Login(form)

    if method == 'GET' or not _form.validate_on_submit():
        for error in _form.errors.items():
            print(error)
        return _.render_template('login.html', form=_form)

    username = form.get('username', None)
    password = form.get('password', None)

    if not all([username, password]):
        return _.redirect(_.url_for('login_user'))

    user = _.User.query.filter_by(username=username).first()

    if user and user.is_valid_passowrd(password):

        _.session['user'] = {
            'id': user.id,
            'username': user.username,
            'name': user.name
        }

        return _.redirect(_.url_for('home'))
    else:
        return _.redirect(_.url_for('login_user'))
