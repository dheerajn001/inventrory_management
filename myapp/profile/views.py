from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_login import login_required
from myapp import db
from myapp.models import User
from myapp.profile.forms import ProfileForm


profile_blueprint = Blueprint('profile', __name__, template_folder='templates/profile')


@profile_blueprint.route('/', methods=['GET','Post'])
@login_required
def profile():
    # form = RegistrationForm()
    user = session['user']
    heading = 'Profile'
    user_id = db.session.query(User.id).filter(User.username == user).first()
    user_name = User.query.filter_by(username=user).one()
    # user = Customer.query.filter_by(id=id).one()
    form = ProfileForm(obj=user_name)
    if form.validate_on_submit():
        user_name = User.query.get(user_id)
        form.populate_obj(user_name)
        db.session.commit()
        flash('Customer details updated Successfully')
        return redirect(url_for('profile.profile'))
    return render_template('profile.html', user=user, heading=heading, form=form)
