from flask import Blueprint, render_template

from db import db_session
from webapp.product.models import Product

blueprint = Blueprint('main_page', __name__)


@blueprint.route('/')
def index():
    products = db_session.query(Product).all()
    return render_template(
        'main_page/index.html',
        page_title='Список товаров',
        products=products,
    )
