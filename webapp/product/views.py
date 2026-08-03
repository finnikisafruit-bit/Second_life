import os
import uuid

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from db import db_session
from webapp.product.forms import AddProductForm, CommentForm, EditProductForm
from webapp.product.models import Comment, Product

UPLOAD_FOLDER = os.path.join('webapp', 'static', 'images', 'products')

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
        file = form.image.data
        filename = secure_filename(file.filename)
        unique_name = f'{uuid.uuid4().hex}_{filename}'
        save_path = os.path.join(UPLOAD_FOLDER, unique_name)
        file.save(save_path)

        new_product = Product(
            title=form.title.data,
            size=str(form.size.data),
            price=form.price.data,
            description=form.description.data,
            city=form.city.data,
            condition=form.condition.data,
            user_id=current_user.id,
            image_filename=unique_name,
        )

        db_session.add(new_product)
        db_session.commit()

        flash('Вы добавили товар')
        return redirect(url_for('product.product_list'))

    flash('Вы ввели неправильные данные')
    return redirect(url_for('product.add_product'))


@blueprint.route('/edit_product/<int:product_id>')
@login_required
def edit_product(product_id):

    product = db_session.get(Product, product_id)

    if product is None:
        flash('Товар не найден')
        return redirect(url_for('main_page.index'))
    if product.user_id != current_user.id:
        flash('Вы не можете редактировать чужой товар')
        return redirect(url_for('product.product_page', product_id=product_id))

    form = EditProductForm()
    form.title.data = product.title
    form.size.data = str(product.size)
    form.price.data = product.price
    form.description.data = product.description
    form.city.data = product.city
    form.condition.data = product.condition
    return render_template(
        'product/edit_product.html',
        page_title='Редактирование товара',
        form=form,
        product=product,
    )


@blueprint.route('/process-edit-product/<int:product_id>', methods=['POST'])
@login_required
def process_edit_product(product_id):
    product = db_session.get(Product, product_id)

    if product is None:
        flash('Товар не найден')
        return redirect(url_for('main_page.index'))
    if product.user_id != current_user.id:
        flash('Вы не можете редактировать чужой товар')
        return redirect(url_for('product.product_page', product_id=product_id))

    form = EditProductForm()

    if form.validate_on_submit():
        product.title = form.title.data
        product.size = str(form.size.data)
        product.price = form.price.data
        product.description = form.description.data
        product.city = form.city.data
        product.condition = form.condition.data
        if form.image.data:
            file = form.image.data
            filename = secure_filename(file.filename)
            unique_name = f'{uuid.uuid4().hex}_{filename}'
            file.save(os.path.join(UPLOAD_FOLDER, unique_name))
            product.image_filename = unique_name
        db_session.commit()

        flash('Вы успешно изменили данные')
        return redirect(url_for('product.product_page', product_id=product.id))

    return render_template(
        'product/edit_product.html',
        page_title='Редактирование товара',
        form=form,
        product=product,
    )


@blueprint.route('/process-add-comment/<int:product_id>', methods=['POST'])
@login_required
def process_add_comment(product_id):
    product = db_session.get(Product, product_id)

    if product is None:
        flash('Товар не найден')
        return redirect(url_for('main_page.index'))

    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(
            user_id=current_user.id,
            product_id=product.id,
            text=form.text.data,
        )

        db_session.add(comment)
        db_session.commit()

        flash('Комментарий добавлен')
        return redirect(url_for('product.product_page', product_id=product.id))
    else:
        flash('Комментарий не добавлен')
        return redirect(url_for('product.product_page', product_id=product.id))


@blueprint.route('/process-delete-comment/<int:comment_id>', methods=['POST'])
@login_required
def process_delete_comment(comment_id):
    comment = db_session.get(Comment, comment_id)

    if comment is None:
        flash('Комментарий не найден')
        return redirect(url_for('main_page.index'))

    if comment.user_id != current_user.id:
        flash('Вы можете удалить только свой комментарий')
        return redirect(url_for('product.product_page', product_id=comment.product.id))

    product_id = comment.product_id
    db_session.delete(comment)
    db_session.commit()
    flash('Комментарий удален')
    return redirect(url_for('product.product_page', product_id=product_id))


@blueprint.route('/edit_comment/<int:comment_id>')
@login_required
def edit_comment(comment_id):
    comment = db_session.get(Comment, comment_id)

    if comment is None:
        flash('Комментарий не найден')
        return redirect(url_for('main_page.index'))
    if comment.user_id != current_user.id:
        flash('Вы можете редактировать только свой комментарий')
        return redirect(url_for('product.product_page', product_id=comment.product_id))

    form = CommentForm()
    form.text.data = comment.text
    return render_template(
        'product/edit_comment.html',
        page_title='редактированиек комментария',
        form=form,
        comment=comment,
    )


@blueprint.route('/process-edit-comment/<int:comment_id>', methods=['POST'])
@login_required
def process_edit_comment(comment_id):
    comment = db_session.get(Comment, comment_id)

    if comment is None:
        flash('Комментарий не найден')
        return redirect(url_for('main_page.index'))
    if comment.user_id != current_user.id:
        flash('Вы можете редактировать только свой комментарий')
        return redirect(url_for('product.product_page', product_id=comment.product_id))

    form = CommentForm()

    if form.validate_on_submit():
        comment.text = form.text.data
        db_session.commit()
        flash('Вы успешно изменили комментарий')
        return redirect(url_for('product.product_page', product_id=comment.product.id))

    return render_template(
        'product/edit_comment.html',
        page_title='Редактирование комментария',
        form=form,
        comment=comment,
    )


@blueprint.route('/<int:product_id>')
def product_page(product_id):
    product = db_session.query(Product).filter_by(id=product_id).first()
    comments = (
        db_session.query(Comment)
        .filter_by(product_id=product_id)
        .order_by(Comment.id)
        .all()
    )
    form = CommentForm()
    return render_template(
        'product/product_page.html',
        product=product,
        comments=comments,
        form=form,
        page_title=f'Карточка товара: {product.title}',
    )
