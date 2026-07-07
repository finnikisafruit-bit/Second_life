from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from db import db_session
from webapp.product.forms import AddProductForm
from webapp.product.models import Product

blueprint = Blueprint('product', __name__, url_prefix='/product')


@blueprint.route('/')
@login_required
def product_list():
    products = db_session.query(Product).filter_by(user_id=current_user.id).all()
    return render_template(
        'product/my_product.html', page_title='Карточки товаров', products=products
    )


@blueprint.route('/add_product')
@login_required
def add_product():
    title = 'Добавление товара'
    add_product_form = AddProductForm()
    return render_template(
        'product/add_product.html', page_title=title, form=add_product_form
    )


@blueprint.route('/process-add_product', methods=['POST'])
@login_required
def process_add_product():
    form = AddProductForm()

    if form.validate_on_submit():
        new_product = Product(
            title=form.title.data,
            size=str(form.size.data),
            price=form.price.data,
            description=form.description.data,
            city=form.city.data,
            condition=form.condition.data,
            user_id=current_user.id,
        )

        db_session.add(new_product)
        db_session.commit()

        flash('Вы добавили товар')
        return redirect(url_for('product.product_list'))

    flash('Вы ввели неправильные данные')
    return redirect(url_for('product.add_product'))


@blueprint.route('/<int:product_id>')
def product_page(product_id):
    product = db_session.query(Product).filter_by(id=product_id).first()
    return render_template(
        'product/product_page.html',
        product=product,
        page_title=f'Карточка товара: {product.title}',
    )
