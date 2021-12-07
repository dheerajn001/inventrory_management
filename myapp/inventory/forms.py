from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, PasswordField, IntegerField, TextAreaField, SelectField, SelectMultipleField)
from wtforms.validators import DataRequired, Email, EqualTo, Length

class AddProduct(FlaskForm):
    item_name = StringField('Product Name', validators=[DataRequired(), Length(max=100)])
    item_price = IntegerField('Price', validators=[DataRequired()])
    item_qty = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Submit')
