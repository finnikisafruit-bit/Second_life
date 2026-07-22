from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)

from db import db_session
from webapp.user.forms import EditProfileForm, LoginForm, RegisterForm
from webapp.user.models import User, Wishlist

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
    return render_template('user/login.html', page_title='Авторизация', form=form)


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
        new_user = User(
            login=form.login.data,
            username=form.username.data,
            email=form.email.data,
            role='user',
        )
        new_user.set_password(form.password.data)

        db_session.add(new_user)
        db_session.commit()

        flash('Вы зарегистрировались')
        return redirect(url_for('user.login'))

    return render_template(
        'user/register.html',
        page_title='Регистрация',
        form=form,
    )


@blueprint.route('/wishlist')
@login_required
def wishlist():
    products = [item.product for item in current_user.wishlist_items]
    return render_template(
        'user/wishlist.html',
        page_title='Избранное',
        products=products,
    )


@blueprint.route('/process-wishlist-add', methods=['POST'])
@login_required
def process_wishlist_add():
    product_id = int(request.form['product_id'])

    exists = (
        db_session.query(Wishlist)
        .filter_by(
            user_id=current_user.id,
            product_id=product_id,
        )
        .first()
    )

    if exists:
        flash('Товар уже в избранном')
    else:
        db_session.add(Wishlist(user_id=current_user.id, product_id=product_id))
        db_session.commit()
        flash('Добавлено в избранное')
    return redirect(url_for('product.product_page', product_id=product_id))


@blueprint.route('/process-wishlist-remove', methods=['POST'])
@login_required
def process_wishlist_remove():
    product_id = int(request.form['product_id'])
    item = (
        db_session.query(Wishlist)
        .filter_by(user_id=current_user.id, product_id=product_id)
        .first()
    )
    if item:
        db_session.delete(item)
        db_session.commit()
        flash('Товар удален из избранного')
    return redirect(url_for('user.wishlist'))


@blueprint.route('/profile')
@login_required
def profile():
    title = 'Профиль пользователя'
    return render_template('user/profile.html', page_title=title)


@blueprint.route('/edit-profile')
@login_required
def edit_profile():

    form = EditProfileForm()
    form.username.data = current_user.username
    form.email.data = current_user.email
    return render_template(
        'user/edit_profile.html',
        page_title='Редактирование профиля',
        form=form,
    )


@blueprint.route('/process-edit-profile', methods=['POST'])
@login_required
def process_edit_profile():
    form = EditProfileForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.password.data:
            current_user.set_password(form.password.data)
        db_session.commit()

        flash('Вы успешно изменили данные')
        return redirect(url_for('user.profile'))

    return render_template(
        'user/edit_profile.html',
        page_title='Редактирование профиля',
        form=form,
    )
