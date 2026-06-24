from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login = StringField(
        'Имя пользователя',
        validators=[DataRequired()],
        render_kw={'class': 'form-control w-25'},
    )
    password = PasswordField(
        'Пароль', validators=[DataRequired()], render_kw={'class': 'form-control w-25'}
    )
    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-primary'})
