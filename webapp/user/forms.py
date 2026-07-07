from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from db import db_session
from webapp.user.models import User


class LoginForm(FlaskForm):
    login = StringField(
        'Имя пользователя',
        validators=[DataRequired()],
        render_kw={'class': 'form-control w-50'},
    )
    password = PasswordField(
        'Пароль', validators=[DataRequired()], render_kw={'class': 'form-control w-50'}
    )

    remember_me = BooleanField('Запомнить меня')

    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-primary'})


class RegisterForm(FlaskForm):
    login = StringField(
        'Ваш логин',
        validators=[DataRequired()],
        render_kw={'class': 'form-control w-50'},
    )
    username = StringField(
        'Имя пользователя',
        validators=[DataRequired()],
        render_kw={'class': 'form-control w-50'},
    )
    email = EmailField(
        'Почта',
        validators=[DataRequired(), Email()],
        render_kw={'class': 'form-control w-50'},
    )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired()],
        render_kw={'class': 'form-control w-50'},
    )
    password1 = PasswordField(
        'Повторите пароль',
        validators=[
            DataRequired(),
            EqualTo('password', message='Пароли не совпадают'),
        ],
        render_kw={'class': 'form-control w-50'},
    )

    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-primary'})

    def validate_login(self, login):
        login_count = db_session.query(User).filter_by(login=login.data).count()
        if login_count > 0:
            raise ValidationError('Пользователь с таким логином уже зарегистрирован')

    def validate_email(self, email):
        email_count = db_session.query(User).filter_by(email=email.data).count()
        if email_count > 0:
            raise ValidationError(
                'Пользователь с такой электронной почтой уже зарегистрирован'
            )
