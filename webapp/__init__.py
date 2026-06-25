from pathlib import Path

from flask import Flask, flash, redirect, render_template, url_for
from flask_login import LoginManager, login_user, logout_user

from db import db_session
from webapp.forms import LoginForm
from webapp.models import User

app = Flask(__name__)
app.config.from_pyfile(str(Path(__file__).parent.parent / 'config.py'))

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return db_session.get(User, int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    title = 'Авторизация'
    login_form = LoginForm()
    return render_template('login.html', page_title=title, form=login_form)


@app.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()

    if form.validate_on_submit():
        user = db_session.query(User).filter_by(login=form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вы успешно  залогинились')
            return redirect(url_for('index'))
    flash('Неправильное имя или пароль')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    logout_user()
    flash('Вы разлогинились')
    return redirect(url_for('index'))


# @app.route('/user')
# def user():
#    return render_template('user.html')


# @app.route('/basket')
# def basket():
#    return render_template('basket.html')


# @app.route('/my_announcement')
# def my_announcement():
#    return render_template('my_announcement.html')


# app.route('/create_announcement')
# def create_announcement():
#    return render_template('create_announcement.html')


if __name__ == '__main__':
    app.run(debug=True)
