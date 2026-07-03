from pathlib import Path

from flask import Flask
from flask_login import (
    LoginManager,
)

from db import db_session
from webapp.admin.views import blueprint as admin_blueprint
from webapp.main_page.views import blueprint as main_page_blueprint
from webapp.product.views import blueprint as product_blueprint
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint

app = Flask(__name__)

app.config.from_pyfile(str(Path(__file__).parent.parent / 'config.py'))


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.login'
app.register_blueprint(admin_blueprint)
app.register_blueprint(main_page_blueprint)
app.register_blueprint(product_blueprint)
app.register_blueprint(user_blueprint)


@login_manager.user_loader
def load_user(user_id):
    return db_session.get(User, int(user_id))


if __name__ == '__main__':
    app.run(debug=True)
