from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class BookForm(FlaskForm):
    name = StringField('Name',
                        validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    published = StringField('Published At', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()])
    image_link = StringField('Image Link', validators=[DataRequired()])
    submit = SubmitField('Add Book')
    
    
