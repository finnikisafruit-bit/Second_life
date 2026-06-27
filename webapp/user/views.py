from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user,
)

from db import db_session
from webapp.user.forms import LoginForm
from webapp.user.models import User

blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_page.index'))
    title = 'Авторизация'
    login_form = LoginForm()
    return render_template('user/login.html', page_title=title, form=login_form)


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()

    if form.validate_on_submit():
        user = db_session.query(User).filter_by(login=form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вы успешно  залогинились')
            return redirect(url_for('main_page.index'))
    flash('Неправильное имя или пароль')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы разлогинились')
    return redirect(url_for('main_page.index'))
