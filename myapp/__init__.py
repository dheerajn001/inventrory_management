from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

app = Flask(__name__)

app.config['SECRET_KEY'] = 'supersecretkeyformyappdonttrytohack'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/inventorytwo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'rahulprojectmail@gmail.com'
app.config['MAIL_PASSWORD'] = 'Inventory@app1234'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

db = SQLAlchemy()

db.init_app(app)
Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

from myapp.user.views import user_blueprint
from myapp.customers.views import customer_blueprint
from myapp.inventory.views import inventory_blueprint
from myapp.invoices.views import invoices_blueprint
from myapp.profile.views import profile_blueprint
from myapp.reports.views import reports_blueprint

app.register_blueprint(user_blueprint, url_prefix='/')
app.register_blueprint(customer_blueprint, url_prefix='/customer')
app.register_blueprint(inventory_blueprint, url_prefix='/inventory')
app.register_blueprint(invoices_blueprint, url_prefix='/invoice')
app.register_blueprint(profile_blueprint, url_prefix='/profile')
app.register_blueprint(reports_blueprint, url_prefix='/report')
