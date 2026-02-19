from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp

accepted_char= Regexp(r"^[A-Za-z]+$") #tillåtna karaktärer, ^start["tillåtna"] +"en eller fler bokstäver" $"slut"

class GuessForm(FlaskForm):
    guess = StringField("Guess", validators=[DataRequired(), Length(min=5, max=5), accepted_char], #server side
    render_kw={"maxlength": 5, "pattern": "[A-za-z]{5}"} #clientside
    )
    
    submit = SubmitField("Submit")