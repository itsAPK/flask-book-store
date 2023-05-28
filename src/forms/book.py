from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField,SelectField,TextAreaField,ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange,InputRequired
from src.models.books import Genre

from src.extensions import EnumSelectField

class BookForm(FlaskForm):
    name = StringField('Name',
                        validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    published = SelectField('Year', choices=[(str(year), str(year)) for year in range(1950, date.today().year + 1)], coerce=int)
    genre =  SelectField('Genre', choices=[(genre.value, genre.name.capitalize()) for genre in Genre], validators=[InputRequired()])
    image_link = StringField('Image Link', validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    in_stock =  IntegerField('Stock',validators=[NumberRange(min=0)])
    show = SelectField('Show ', choices=[ 'Yes',  'No'])
    submit = SubmitField('Add Book')
    

class BookUpdateForm(FlaskForm):
    name = StringField('Name',
                        validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    published = SelectField('Year', choices=[(str(year), str(year)) for year in range(1950, date.today().year + 1)], coerce=int)
    genre =  EnumSelectField(enum=Genre)
    image_link = StringField('Image Link', validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    in_stock = IntegerField('Stock',validators=[NumberRange(min=0)])
    show = SelectField('Show ', choices=[True, False])
    submit = SubmitField('Update Book')
