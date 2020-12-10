url = '/register'
methods = ['POST', 'GET']
policy = ['not_authorized']


def app(_, method, form, querystring, *args, **kwargs):

    _form = _.Form_Register(form)

    if method == 'GET' or not _form.validate_on_submit():
        for error in _form.errors.items():
            print(error)
        return _.render_template('register.html', form=_form)

    if _.User.query.filter_by(username=form.get('username')).first():
        return 'username exists'

    user = _.User.create_by_form(
        form,
        _.User.name,
        _.User.username,
        _.User.password
    )

    user.save()
    return _.redirect(_.url_for('login_user'))
