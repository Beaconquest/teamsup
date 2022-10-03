from datetime import datetime

# Flask object and database imports
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

# Login object declaration imports
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash

# Form object declaration imports
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, length, EqualTo, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-password-supreme'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myTeamDatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# define database models
# User class 
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), index=True)
    role = db.Column(db.String(140), index=True)
    email = db.Column(db.String(140), index=True, unique=True)
    username = db.Column(db.String(140), index=True, unique=True)
    password_hash = db.column(db.String(140))
    joined_at_date = db.Column(db.DateTime(), index=True, default=datetime.utcnow)

    def __repr__(self):
        return f"< {self.role} {self.name}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

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
    role = SelectField('Role', [DataRequired()], 
    roles=[
        "Head Coach", "Assistant Coach", "Team Manager", "Volunteer"
    ])
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
    position = StringField('Position')
    submit = SubmitField('Register')

class ContactForm(FlaskForm):
    """Contact Form."""
    name = StringField('Name', [DataRequired()])
    email = StringField(
        'Email',
        [
            #Email(message=('Not a valid email address.')), 
            DataRequired()]
    )
    body = TextAreaField(
        'Message', 
        [DataRequired(), length(min=5, message=("Your message is too short."))]
    )
    #recaptcha = RecaptchaField()
    submit = SubmitField('Submit')

# app routes

@app.route('/register', methods=["GET", "POST"])
def register():
    """Registration form."""
    form = RegistrationForm(csfr_enable=False)
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            role=form.role.data,
            username=form.username.data,
            email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
    return render_template('register.html', title='Register', template_form=form)

@app.route('/register/athlete', methods=["GET", "POST"])
def athlete():
    """Athlete Registration Form."""
    form = AthleteRegistrationForm(csfr_enable=False)
    if form.validate_on_submit():
        athlete = Athlete(
            athlete_name=form.athlete_name.data,
            date_of_birth=form.date_of_birth.data,
            student_id=form.student_id.data,
            position=form.position.data
        )
        db.session.add(athlete)
        db.session.commit()
    return render_template("athlete.html", title="Athlete", template_form=form)

@app.route('/register/team', methods=["GET", "POST"])
def team():
    """Team Registration Form."""
    form = TeamRegistrationForm(csfr_enable=False)
    if form.validate_on_submit():
        team = Team(team_name=form.team_name.data)
        db.session.add(team)
        db.session.commit()
    return render_template("team.html", title='Team', template_form=form)

@app.route('/contact', methods=["GET", "POST"])
def contact():
    """Standard contact form."""
    form = ContactForm()
    if form.validate_on_submit():
        return redirect(url_for("Success"))
    return render_template('contact.html', template_form=form)

@app.route('/')
def index():
    return render_template('index.html')
