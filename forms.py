from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class GuessForm(FlaskForm):
    guess = StringField("Guess", validators=[DataRequired()])
    submit = SubmitField("Submit")