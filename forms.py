from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import DataRequired, Length

class RecordForm(FlaskForm):
    value = FloatField('Enter float number:', [DataRequired()])
    submit = SubmitField('Submit')