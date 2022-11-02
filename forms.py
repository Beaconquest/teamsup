from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, RadioField, BooleanField
from wtforms.validators import DataRequired, length, EqualTo, Email

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    role = RadioField('Role', [DataRequired()], 
    choices=[
        "Head Coach", "Assistant Coach", "Team Manager", "Volunteer"
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class TeamRegistrationForm(FlaskForm):
    team_name = StringField('Team Name', validators=[DataRequired()])
    submit = SubmitField('Register')
    
class AthleteRegistrationForm(FlaskForm):
    athlete_name = StringField('Athletes Name', validators=[DataRequired()])
    date_of_birth = StringField('DOB', validators=[DataRequired()])
    student_id = IntegerField('StudentID', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    submit = SubmitField('Register')

class ContactForm(FlaskForm):
    """Contact Form."""
    name = StringField('Name', validators=[DataRequired()])
    email = StringField(
        'Email', validators=[
            Email(), 
            DataRequired()]
    )
    body = TextAreaField(
        'Message', 
        [DataRequired(), length(min=5, message=("Your message is too short."))]
    )
    # register recaptcha with google  
    #recaptcha = RecaptchaField()
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')