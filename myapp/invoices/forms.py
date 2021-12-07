from flask_wtf import FlaskForm
from wtforms import (SubmitField, IntegerField, SelectField)
from wtforms.validators import DataRequired

class CreateBill(FlaskForm):
    customer = SelectField('Select Customer', choices=[])
    products = SelectField('Select Product', choices=[])
    item_qty = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Add To Bill')



class InvoiceForm(FlaskForm):
    products = SelectField('Products', choices=[])
    item_qty = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Add To Cart')