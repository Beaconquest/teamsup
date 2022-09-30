from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, EqualTo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-password-supreme'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myTeamDatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# define database models
class Coach(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), index=True)
    email = db.Column(db.String(140), index=True, unique=True)
    username = db.Column(db.String(140), index=True, unique=True)
    password_hash = db.column(db.String(140))
    joined_at_date = db.Column(db.DateTime(), index=True, default=datetime.utcnow)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(140), index=True, unique=True)

class Athlete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    athlete_name = db.Column(db.String, index=True)
    date_of_birth = db.Column(db.String, index=True)
    student_id = db.Column(db.Integer, index=True, unique=True)
    position = db.Column(db.String, index=True)

# set up database
# db.create_all()

# define FlaskForm 
class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class TeamRegistrationForm(FlaskForm):
    team_name = StringField('Team Name', validators=[DataRequired()])
    submit = SubmitField('Register')
    
class AthleteRegistrationForm(FlaskForm):
    athlete_name = StringField('Athletes Name', validators=[DataRequired()])
    date_of_birth = StringField('DOB')
    student_id = IntegerField('StudentID' )
    submit = SubmitField('Register')

@app.route('/register')
def register():
    form = RegistrationForm(csfr_enable=False)
    return render_template('register.html', template_form=form)

@app.route('/register/athlete')
def athlete():
    form = AthleteRegistrationForm(csfr_enable=False)
    return render_template("athlete.html", template_form=form)

@app.route('/register/team')
def team():
    form = TeamRegistrationForm(csfr_enable=False)
    return render_template("team.html", template_form=form)

@app.route('/')
def index():
    return render_template('index.html')
