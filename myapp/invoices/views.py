from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_login import login_required
from myapp import db, mail
from flask_mail import Message
from myapp.models import User, Billing, Stock, Customer, Cart
from myapp.invoices.forms import (InvoiceForm)
from sqlalchemy import func

invoices_blueprint = Blueprint('invoice', __name__, template_folder='templates/invoices')

@invoices_blueprint.route('/')
@login_required
def invoices():
    user = session['user']
    heading = 'Invoices'
    user_name = db.session.query(User.id).filter(User.username == user).first()
    view_customers = Customer.query.filter_by(user_id=user_name.id).all()
    return render_template('invoices.html', user=user, heading=heading, view_customers=view_customers)



@invoices_blueprint.route('/viewbill/<string:id>')
@login_required
def viewbill(id):
    user = session['user']
    view_bill = Cart.query.filter_by(customer_id=id).all()
    final_amount = Cart.query.with_entities(func.sum(Cart.total_amount).label("totalamount")).filter_by(customer_id=id).first()
    totalamt = final_amount.totalamount
    if totalamt is None:
        flash('Invoice is Empty!')
        return redirect(url_for('invoice.invoices'))
    else:
        for customern in view_bill:
            customerr = customern.customer_name
            return render_template('viewbill.html', view_bill=view_bill, totalamt=totalamt, id=id, user=user, customerr=customerr)


@invoices_blueprint.route('/createinvoice/<string:id>', methods=['GET', 'POST'])
@login_required
def createinvoice(id):
    user = session['user']
    form = InvoiceForm()
    customer_fname = db.session.query(Customer.firstname).filter(Customer.id == id).first()
    customer_lname = db.session.query(Customer.lastname).filter(Customer.id == id).first()

    user_name = db.session.query(User.id).filter(User.username == user).first()
    view_products = Stock.query.filter_by(user_id=user_name.id).all()
    form.products.choices = [(products.id, products.item_name) for products in view_products]

    final_amount = Cart.query.with_entities(func.sum(Cart.total_amount).label("totalamount")).filter_by(
        customer_id=id).first()
    totalamt = final_amount.totalamount

    if form.validate_on_submit():
        customer_name = db.session.query(Customer.email).filter(Customer.id == id).first()
        s_products = form.products.data
        product_name = db.session.query(Stock.item_name).filter(Stock.id == s_products).first()

        items = Stock.query.filter_by(id=s_products).first()

        quantity = form.item_qty.data
        if quantity > items.item_qty:
            flash('Not enough stock available of selected product!!')
            return render_template('createinvoice.html', form=form, customer_fname=customer_fname[0],
                                   customer_lname=customer_lname[0], id=id, user=user)
        else:
            product_price = db.session.query(Stock.item_price).filter(Stock.id == s_products).first()

            total = int(quantity) * int(product_price[0])

            invoice = Cart(customer_name=customer_name[0], item_name=product_name[0], item_price=product_price[0],
                              item_quantity=quantity, total_amount=total, user_id=user_name.id, customer_id=id)
            db.session.add(invoice)

            product_quantity = db.session.query(Stock.item_qty).filter(Stock.id == s_products).first()
            available_quantity = product_quantity[0] - quantity

            items.item_qty = available_quantity

            db.session.commit()
            flash('Product added to Cart Successfully!!!')

            user_email = db.session.query(User.email).filter(User.username == user).first()
            useremail = user_email[0]

            if available_quantity < 10:

                prod_name = db.session.query(Stock.item_name).filter(Stock.id == s_products).first()
                flash('Available quantity is less than 10. Total available quantity is: '+ str(available_quantity))
                quantity_alert = 'You will soon run out of quantity of product: ' \
                                 + prod_name[0] + '\nPlease update your stock as soon as possible'
                msg = Message(
                    'Quantity Alert',
                    sender='rahulprojectmail@gmail.com',
                    recipients=[useremail]
                )
                msg.body = quantity_alert
                mail.send(msg)


            final_amt = Cart.query.with_entities(func.sum(Cart.total_amount).label("totalamount")).filter_by(
                customer_id=id).first()
            totalamtn = final_amt.totalamount

            view_bill = Cart.query.filter_by(customer_id=id).all()

            for customern in view_bill:
                customerr = customern.customer_name
                return render_template('createinvoice.html', form=form, customerr=customerr, totalamt=totalamt,
                                       view_bill=view_bill, customer_fname=customer_fname[0],
                                       customer_lname=customer_lname[0], totalamtn=totalamtn, id=id, user=user)
    return render_template('createinvoice.html', view_products=view_products, form=form,
                           customer_fname=customer_fname[0], customer_lname=customer_lname[0],
                           totalamt=totalamt, id=id, user=user)



@invoices_blueprint.route('/billing/<string:id>', methods=['GET', 'POST'])
@login_required
def billing(id):
    user = session['user']
    user_name = db.session.query(User.id).filter(User.username == user).first()
    final_amount = Cart.query.with_entities(func.sum(Cart.total_amount).label("totalamount")).filter_by(customer_id=id).first()

    totalamt = final_amount.totalamount
    if totalamt is None:
        flash('Invoice is Empty! Click on Create Bill to create new one!')
        return redirect(url_for('customer.customers'))
    else:
        customer_name = db.session.query(Customer.email).filter(Customer.id == id).first()
        bill = Billing(customer_name=customer_name[0], total_amount=totalamt, user_id=user_name.id)
        db.session.add(bill)

        Cart.query.filter_by(customer_id=id).delete()

        db.session.commit()
        emailid = customer_name[0]
        msg = Message(
            'Bill Generated',
            sender='rahulprojectmail@gmail.com',
            recipients=[emailid]
        )
        msg.body = 'Your bill amount is: ' + str(totalamt)
        mail.send(msg)

        # flash('Bill has been generated!!')

        return render_template('billing.html', cost=totalamt, customer_name=customer_name[0], user=user)

