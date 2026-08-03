from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import (
    FloatField,
    IntegerField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length


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
    image = FileField(
        'Фото товара',
        validators=[
            FileRequired(),
            FileAllowed(['jpg', 'jpeg', 'png', 'webp', 'gif'], 'Только изображения'),
        ],
    )
    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-primary'})


class EditProductForm(FlaskForm):
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
    image = FileField(
        'Изменить фото',
        validators=[
            FileAllowed(['jpg', 'jpeg', 'png', 'webp', 'gif'], 'Только изображения'),
        ],
    )
    submit = SubmitField('Сохранить', render_kw={'class': 'btn btn-primary'})


class CommentForm(FlaskForm):
    text = TextAreaField(
        'Комментарий',
        validators=[DataRequired(), Length(max=300)],
        render_kw={'class': 'form-control', 'rows': 3},
    )
    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-primary'})
