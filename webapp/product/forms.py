from flask_wtf import FlaskForm
from wtforms import (
    FloatField,
    IntegerField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired


class AddProductForm(FlaskForm):
    title = StringField(
        'Наименование',
        validators=[DataRequired()],
        render_kw={'class': 'form-control w-50'},
    )
    size = FloatField(
        'Размер',
        validators=[DataRequired()],
        render_kw={'class': 'form-control w-50'},
    )  # у меня только обувь, поэтому FloatField
    price = IntegerField(
        'Цена, ₽',
        validators=[DataRequired()],
        render_kw={'class': 'form-control w-50'},
    )
    description = TextAreaField(
        'Описание',
        validators=[DataRequired()],
        render_kw={'class': 'form-control w-75'},
    )
    city = StringField(
        'Город',
        validators=[DataRequired()],
        render_kw={'class': 'form-control w-50'},
    )
    condition = StringField(
        'Состояние',
        validators=[DataRequired()],
        render_kw={'class': 'form-control w-50'},
    )

    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-primary'})
