from flask import (Blueprint, render_template, redirect, g, url_for, flash,
                   request)
from flask.ext.login import login_user, logout_user

from aurora_app import login_manager
from aurora_app.models import User
from aurora_app.decorators import public
from aurora_app.forms import LoginForm

mod = Blueprint('main', __name__)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@mod.route('/')
def index():
    return render_template('main/index.html')


@mod.route('/login', methods=['GET', 'POST'])
@public
def login():
    if g.user is not None:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next = request.args.get('next', False)
            return (redirect(next) if next else
                    redirect(url_for('main.index')))
        else:
            flash(u'Invalid username or password!')

    return render_template('main/login.html', form=form)


@mod.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
