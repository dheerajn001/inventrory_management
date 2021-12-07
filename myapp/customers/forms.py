from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, TextAreaField)
from wtforms.validators import DataRequired, Email, Length

class AddCustomer(FlaskForm):
    firstname = StringField('Name', validators=[DataRequired(), Length(min=3, max=50)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(message='Please enter valid email!'), Length(min=7, max=150)])
    address = TextAreaField('Address', validators=[Length(max=200)])
    submit = SubmitField('Submit')
