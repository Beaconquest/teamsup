from flask import render_template, request, redirect, url_for, flash
from flask_package import app, db
from flask_login import login_required, login_user, logout_user, current_user
from flask_package.forms import RegistrationForm, AthleteRegistrationForm, StaffRegistrationForm, TeamRegistrationForm, ContactForm, LoginForm
from flask_package.models import User, Athlete, Team, Staff, Contact

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

@app.route('/register/staff', methods=["GET", "POST"])
@login_required
def register_staff():
    """Registration form."""

    staff_members = Staff.query.filter_by(coach_id=current_user.id)
    if staff_members is None:
        staff_members = []

    form = StaffRegistrationForm(csfr_enable=False)

    if form.validate_on_submit():
        staff = Staff(
            name=form.staff_name.data,
            email=form.staff_email.data,
            role=form.role.data)
        db.session.add(staff)
        db.session.commit()
        flash("Account created!")
        return redirect('/coaches')

    return render_template('register-staff.html', title='RegisterStaff', staff_members=staff_members, template_form=form)

@app.route('/register/athlete', methods=["GET", "POST"])
@login_required
def register_athlete():
    """Athlete Registration Form."""

    athletes = Athlete.query.filter_by(coach_id=current_user.id)
    if athletes is None:
        athletes = []

    form = AthleteRegistrationForm(csfr_enable=False)
    if form.validate_on_submit():
        athlete = Athlete(
            name=form.name.data,
            date_of_birth=form.date_of_birth.data,
            student_id=form.student_id.data,
            position=form.position.data
        )
        db.session.add(athlete)
        db.session.commit()
        return redirect('/athletes')
    return render_template("register-athlete.html", title="RegisterAthlete", athletes=athletes, template_form=form)

@app.route('/athletes')
@login_required
def athletes():
    athletes = Athlete.query.all()
    return render_template('athletes.html', athletes=athletes)

@app.route('/register/team', methods=["GET", "POST"])
@login_required
def register_team():
    """Team Registration Form."""
    
    if current_user.role == 'Head Coach':

        teams = Team.query.filter_by(coach_id=current_user.id)
        if teams is None:
            teams = []        
        form = TeamRegistrationForm(csfr_enable=False)
        if form.validate_on_submit():
            team = Team(
                team_name = form.team_name.data,
                coach_id = current_user.id
            )
            db.session.add(team)
            db.session.commit()
            return redirect('/team')
    return render_template("register-team.html", title='Team', teams=teams, template_form=form)

@app.route('/team')
@login_required
def team():
    teams = Team.query.filter_by(coach_id=current_user.id)
    
    if teams is None:
            teams = [] 
    
    return render_template('team.html', teams=teams)

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
    teams = Team.query.filter_by(coach_id=user.id)

    return render_template('user.html', user=user, teams=teams)

@app.route('/coaches')
@login_required
def coaches():
    coaches = User.query.filter_by(id=current_user.id)
    staff = Staff.query.all()
    return render_template('coaches.html', coaches=coaches, staff=staff)

# contact page 
@app.route('/contact', methods=["GET", "POST"])
def contact():
    """Standard contact form."""
    form = ContactForm(csfr_enable=False)
    if form.validate_on_submit():
        contacts = Contact(
            name = form.name.data,
            email = form.email.data,
            body = form.body.data
        )
        db.session.add(contacts)
        db.session.commit()
        flash("We have received your contact.")
    return render_template('contact.html', template_form=form)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404