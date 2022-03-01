from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField 
from wtforms.validators import DataRequired

class Todo(FlaskForm):
    content = TextAreaField(validators=[DataRequired()])
    submit = SubmitField('Submit todo')