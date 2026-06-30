from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


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
