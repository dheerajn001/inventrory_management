from flask import Blueprint, render_template, redirect, url_for, flash, session, Markup
from flask_login import login_required
from myapp import db
from myapp.models import User, Customer
from myapp.customers.forms import AddCustomer


customer_blueprint = Blueprint('customer', __name__, template_folder='templates/customers')


@customer_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def customers():
    heading = 'Customers'
    user = session['user']
    user_name = db.session.query(User.id).filter(User.username == user).first()
    view_customers = Customer.query.filter_by(user_id=user_name.id)
    return render_template('customers.html', view_customers=view_customers, user=user, heading=heading)


@customer_blueprint.route('/addcustomer', methods=['GET', 'POST'])
@login_required
def addcustomer():
    form = AddCustomer()
    user = session['user']
    heading = 'Add New Customer'

    if form.validate_on_submit():
        user_name = db.session.query(User).filter(User.username == user).first()

        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        address = form.address.data
        customer = Customer.query.filter_by(email=email, user_id=user_name.id).first()
        if customer:
            flash(Markup('Customer already exists'))
            return redirect(url_for('customer.addcustomer'))
        else:
            add_customer = Customer(firstname=firstname, lastname=lastname, email=email, address=address,
                                    user_id=user_name.id)
            db.session.add(add_customer)
            db.session.commit()
            flash(Markup('Customer added successfully! To view customers <a href="customers" class="alert-link">'
                         'click here</a>'))
            return redirect(url_for('customer.addcustomer'))
    return render_template('addcustomer.html', form=form, user=user, heading=heading)


@customer_blueprint.route('/updatecustomer/<string:id>', methods=['GET', 'POST'])
@login_required
def updatecustomer(id):
    user = session['user']
    heading = 'Add New Customer'
    customer = Customer.query.filter_by(id=id).one()
    form = AddCustomer(obj=customer)
    if form.validate_on_submit():
        customer = Customer.query.get(id)
        form.populate_obj(customer)
        db.session.commit()
        flash('Customer details updated Successfully')
        return redirect(url_for('customer.customers'))
    return render_template('addcustomer.html', form=form, user=user, heading=heading)


@customer_blueprint.route('/deletecustomer/<string:id>')
@login_required
def deletecustomer(id):
    Customer.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Customer has been deleted!')
    return redirect(url_for('customer.customers'))