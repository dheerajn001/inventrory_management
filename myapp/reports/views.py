from flask import Blueprint, render_template, session
from flask_login import login_required
from myapp import db
from myapp.models import User, Billing
from sqlalchemy import func

reports_blueprint = Blueprint('reports', __name__, template_folder='templates/reports')


@reports_blueprint.route('/')
@login_required
def reports():
    user = session['user']
    heading = 'Reports'
    user_name = db.session.query(User.id).filter(User.username == user).first()
    view_bill = Billing.query.filter_by(user_id=user_name.id).all()
    final_amount = Billing.query.with_entities(func.sum(Billing.total_amount).label("totalamount")).filter_by(user_id=user_name.id).first()
    totalamt = final_amount.totalamount
    return render_template('reports.html', user=user, heading=heading, view_bill=view_bill, totalamt=totalamt)
