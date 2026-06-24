from pathlib import Path

from flask import Flask, render_template

from webapp.forms import LoginForm

app = Flask(__name__)
app.config.from_pyfile(str(Path(__file__).parent.parent / 'config.py'))
# @login_manager.user_loader
# def load_user(user_id):
#    return db_session.get(User, int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    title = 'Авторизация'
    login_form = LoginForm()
    return render_template('login.html', page_title=title, form=login_form)


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
