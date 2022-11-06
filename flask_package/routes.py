from flask import render_template, request, redirect, url_for, flash
from flask_package import app, db
from flask_login import login_required, login_user, logout_user, current_user
from flask_package.forms import RegistrationForm, AthleteRegistrationForm, TeamRegistrationForm, ContactForm, LoginForm
from flask_package.models import User, Athlete, Team

@app.route('/register', methods=["GET", "POST"])
def register():
    """Registration form."""
    if current_user.is_authenticated:
            return redirect(url_for('index'))

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
        flash("Account created!")
        return redirect('/index')

    return render_template('register.html', title='Register', template_form=form)

@app.route('/register/athlete-registration', methods=["GET", "POST"])
@login_required
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
    return render_template("athlete-registration.html", title="Athlete", template_form=form)

@app.route('/register/team', methods=["GET", "POST"])
def team():
    """Team Registration Form."""
    form = TeamRegistrationForm(csfr_enable=False)
    if form.validate_on_submit():
        team = Team(team_name=form.team_name.data)
        db.session.add(team)
        db.session.commit()
    return render_template("team.html", title='Team', template_form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm(csrf_enable=False)
    if form.validate_on_submit():
        
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index', _external=True, _scheme='http'))
        else:
            return redirect(url_for('login', _external=True, _scheme='http'))
    return render_template('login.html', template_form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Login_required routes
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', template_form=user)

@app.route('/coaches')
@login_required
def coaches():
    coaches = User.query.all()
    return render_template('coaches.html', coaches=coaches)

# contact page 
@app.route('/contact', methods=["GET", "POST"])
def contact():
    """Standard contact form."""
    form = ContactForm()
    if form.validate_on_submit():
        return redirect(url_for("Success"))
    return render_template('contact.html', template_form=form)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404