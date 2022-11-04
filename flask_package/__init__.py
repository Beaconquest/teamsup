from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-password-supreme'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myTeamDatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager(app)

from flask_package import routes
from flask_package import models

with app.app_context():
    db.create_all()