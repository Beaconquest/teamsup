from datetime import datetime

# Flask object and database imports
from flask import Flask, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy

# forms
import forms

# Login object declaration imports
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-password-supreme'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myTeamDatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# create login manager
login_manager = LoginManager()
login_manager.init_app(app)


# define database models
# User class 
class User(UserMixin, db.Model):
    
    __tablename__ ='user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), index=True, unique=False)
    role = db.Column(db.String(140), index=True, unique=False)
    email = db.Column(db.String(140), index=True, unique=True)
    username = db.Column(db.String(140), index=True, unique=True)
    password_hash = db.Column(db.String(140))
    joined_at_date = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

    def get_id(self):
        return str(self.id)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'resete_password': self.id, 'exp': time() + expires_in}, 
        current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
    
    def __repr__(self):
        return f"< {self.role} {self.name}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(140), index=True, unique=True)
    users = db.relationship("User", backref='team', lazy='dynamic')
    athletes = db.relationship("Athlete", backref='team', lazy='dynamic')

    def __repr__(self):
        return f"Team: {self.team_name}"

class Athlete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String, index=True, unique=False)
    date_of_birth = db.Column(db.String, index=True, unique=False)
    student_id = db.Column(db.Integer, index=True, unique=True)
    position = db.Column(db.Integer, index=True, unique=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

    def __repr__(self):
        return f"{self.student_name} {self.date_of_birth} {self.student_id} {self.position}"

# set up database
db.create_all()

# registration related routes
@app.route('/register', methods=["GET", "POST"])
def register():
    """Registration form."""
    form = forms.RegistrationForm(csfr_enable=False)
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

@app.route('/register/athlete-registration', methods=["GET", "POST"])
@login_required
def athlete():
    """Athlete Registration Form."""
    form = forms.AthleteRegistrationForm(csfr_enable=False)
    if form.validate_on_submit():
        athlete = Athlete(
            athlete_name=form.athlete_name.data,
            date_of_birth=form.date_of_birth.data,
            student_id=form.student_id.data,
            position=form.position.data
        )
        db.session.add(athlete)
        db.session.commit()
    return render_template("athlete-registration.html", title="Athlete", template_form=form)

@app.route('/register/team', methods=["GET", "POST"])
def team():
    """Team Registration Form."""
    form = forms.TeamRegistrationForm(csfr_enable=False)
    if form.validate_on_submit():
        team = Team(team_name=form.team_name.data)
        db.session.add(team)
        db.session.commit()
    return render_template("team.html", title='Team', template_form=form)

# user login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=["GET", "POST"])
def login():
    form = forms.LoginForm(csrf_enable=False)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('user', _external=True, _scheme='http'))
        else:
            return redirect(url_for('login', _external=True, _scheme='http'))
    return render_template('login.html', template_form=form)

# Login related routes
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', template_form=user)

# contact page 
@app.route('/contact', methods=["GET", "POST"])
def contact():
    """Standard contact form."""
    form = forms.ContactForm()
    if form.validate_on_submit():
        return redirect(url_for("Success"))
    return render_template('contact.html', template_form=form)

@app.route('/')
@app.route('/index')
def index():
    current_users = User.query.all()
    return render_template('index.html', current_users=current_users, template_form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)