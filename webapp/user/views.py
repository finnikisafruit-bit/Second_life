from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user,
)

from db import db_session
from webapp.user.forms import LoginForm, RegisterForm
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


@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_page.index'))
    title = 'Регистрация'
    register_form = RegisterForm()
    return render_template('user/register.html', page_title=title, form=register_form)


@blueprint.route('/process-register', methods=['POST'])
def process_register():
    form = RegisterForm()

    if form.validate_on_submit():
        if db_session.query(User).filter_by(login=form.login.data).first():
            flash('Пользователь с таким логином уже существует')
            return redirect(url_for('user.register'))

        if db_session.query(User).filter_by(email=form.email.data).first():
            flash('Пользователь с такой почтой уже существует')
            return redirect(url_for('user.register'))

        new_user = User(login=form.login.data, email=form.email.data, role='user')
        new_user.set_password(form.password.data)

        db_session.add(new_user)
        db_session.commit()

        flash('Вы зарегистрировались')
        return redirect(url_for('user.login'))

    flash('Вы ввели неправильные данные')
    return redirect(url_for('user.register'))
