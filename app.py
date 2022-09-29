from enum import unique
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-password-supreme'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myTeamDatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# define database models
class Coach(UserMixin, db.Model):
    id = db.Colmun(db.Integer, primary_key=True)
    name = db.Column(db.String(140), index=True)
    email = db.Column(db.String(140), index=True, unique=True)
    username = db.Column(db.String(140), index=True, unique=True)
    password_hash = db.column(db.String(140))
    joined_at_date = db.Column(db.DateTime(), index=True, default=datetime.utc.now)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(140), index=True, unique=True)


class Athlete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    athlete_name = db.Column(db.String, index=True)
    position = db.Column(db.String, index=True)

@app.route('/')
def index():
    return render_template('index.html')
