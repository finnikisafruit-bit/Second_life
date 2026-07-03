from flask import Blueprint, render_template

blueprint = Blueprint('product', __name__, url_prefix='/product')


@blueprint.route('/')
def product_list():
    return render_template('product/product.html', page_title='Карточка товара')
