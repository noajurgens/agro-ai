from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired
"""
Created on Mon Apr  8 3:33:33 2024
@author: Temi
"""

class LabelForm(FlaskForm):
    """
    A FlaskForm for labeling items as 'Healthy' or 'Unhealthy'.

    Attributes:
        choice (RadioField): A field presenting the options 'Healthy' and 'Unhealthy' for the user to choose from.
                             Validation ensures the field cannot be left empty.
        submit (SubmitField): A button for submitting the form.
    """
    choice = RadioField(u'Label', choices=[('H', u'Healthy'), ('B', u'Unhealthy')], validators = [DataRequired(message='Cannot be empty')])
    submit = SubmitField('Confirm')