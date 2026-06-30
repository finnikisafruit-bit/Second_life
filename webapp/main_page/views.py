from flask import Blueprint, render_template

blueprint = Blueprint('main_page', __name__)


@blueprint.route('/')
def index():
    return render_template('main_page/index.html', page_title='Список товаров')
