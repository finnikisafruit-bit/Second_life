from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


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
