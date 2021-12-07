from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, PasswordField)
from wtforms.validators import DataRequired, Email, EqualTo, Length

class ProfileForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=3, max=50)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()],  render_kw={'disabled':'disabled'})
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)], render_kw={'disabled':'disabled'})
    password = PasswordField('New Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Update')