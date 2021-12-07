from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from flask_login import login_user, login_required, logout_user
from myapp import db, mail
from flask_mail import Message
from myapp.models import User, Billing, Stock, Customer
from myapp.user.forms import (RegistrationForm, LoginForm)
from sqlalchemy import func

user_blueprint = Blueprint('users', __name__, template_folder='templates/user')

@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = User.query.filter_by(email=form.email.data).first()
        if email is None:
            username = User.query.filter_by(username=form.username.data).first()
            if username is None:
                register = User(firstname=form.firstname.data, lastname=form.lastname.data,
                                email=form.email.data, username=form.username.data, password=form.password.data)
                db.session.add(register)
                db.session.commit()
                flash('Congrats you have registered successfully!, Please check your inbox')
                welcome = form.firstname.data + ' ' + form.lastname.data + ' Welcome to Inventory Management System'
                msg = Message(
                    'Welcome',
                    sender='rahulprojectmail@gmail.com',
                    recipients=[form.email.data]
                )
                msg.body = welcome
                mail.send(msg)

                return redirect(url_for('users.login'))
            else:
                flash('Username already exists, please try again!')
                return redirect(url_for('users.register'))
        else:
            flash('Email already exists, please try logging in!')
            return redirect(url_for('users.register'))

    return render_template('signup.html', form=form)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            if user.check_password(form.password.data):
                session['user'] = form.username.data
                login_user(user)
                next = request.args.get('next')
                if next == None or not next[0] == '/':
                    next = url_for('users.dashboard')
                return redirect(next)
        flash('Username/password not found!')
        return redirect(url_for('users.login'))
    return render_template('login.html', form=form)


@user_blueprint.route('/dashboard')
@login_required
def dashboard():
    user = session['user']
    heading = 'Dashboard'
    user_name = db.session.query(User.id).filter(User.username == user).first()
    c_rows = db.session.query(Customer).filter_by(user_id=user_name.id).count()
    s_rows = db.session.query(Stock).filter_by(user_id=user_name.id).count()
    final_amount = Billing.query.with_entities(func.sum(Billing.total_amount).label("totalamount")).filter_by(user_id=user_name.id).first()
    totalamt = final_amount.totalamount
    return render_template('dashboard.html', user=user, heading=heading,
                           totalamt=totalamt, c_rows=c_rows, s_rows=s_rows)


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))
