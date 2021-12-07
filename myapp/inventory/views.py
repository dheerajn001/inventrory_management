from flask import Blueprint, render_template, redirect, url_for, flash, session, Markup
from flask_login import login_required
from myapp import db
from myapp.models import User, Stock
from myapp.inventory.forms import AddProduct

inventory_blueprint = Blueprint('inventory', __name__, template_folder='templates/inventory')


@inventory_blueprint.route('/')
@login_required
def inventory():
    user = session['user']
    heading = 'Inventory'
    prod_name = db.session.query(User.id).filter(User.username == user).first()
    view_products = Stock.query.filter_by(user_id=prod_name.id)
    return render_template('inventory.html', user=user, heading=heading, view_products=view_products)


@inventory_blueprint.route('/addproduct', methods=['GET', 'POST'])
@login_required
def addproduct():
    form = AddProduct()
    user = session['user']
    heading = 'Add New Product'

    if form.validate_on_submit():
        user_name = db.session.query(User).filter(User.username == user).first()

        item_name = form.item_name.data
        item_price = form.item_price.data
        item_qty = form.item_qty.data
        item = Stock.query.filter_by(item_name=item_name, user_id=user_name.id).first()
        if item:
            flash('Product already exists')
            return redirect(url_for('inventory.addproduct'))
        else:
            add_product = Stock(item_name=item_name, item_price=item_price, item_qty=item_qty, user_id=user_name.id)
            db.session.add(add_product)
            db.session.commit()
            flash(Markup('Product added successfully! To view products <a href="/inventory/inventory" '
                         'class="alert-link">click here</a>'))
            return redirect(url_for('inventory.addproduct'))
    return render_template('addproduct.html', form=form, heading=heading)


@inventory_blueprint.route('/updateproduct/<string:id>', methods=['GET', 'POST'])
@login_required
def updateproduct(id):
    user = session['user']
    heading = 'Update Product Details'
    product = Stock.query.filter_by(id=id).one()
    form = AddProduct(obj=product)
    if form.validate_on_submit():
        product = Stock.query.get(id)
        form.populate_obj(product)
        db.session.commit()
        flash('Product details updated Successfully')
        return redirect(url_for('inventory.inventory'))
    return render_template('addproduct.html', form=form,  user=user, heading=heading)


@inventory_blueprint.route('/deleteproduct/<string:id>')
@login_required
def deleteproduct(id):
    Stock.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Product has been deleted!')
    return redirect(url_for('inventory.inventory'))
