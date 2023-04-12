from flask import render_template, request, redirect, url_for, flash
from flask_package import app, db
from flask_login import login_required, login_user, logout_user, current_user
from flask_package.forms import RegistrationForm, AthleteRegistrationForm, StaffRegistrationForm, TeamRegistrationForm, ContactForm, LoginForm
from flask_package.models import User, Athlete, Team, Staff, Contact

@app.route('/register', methods=["GET", "POST"])
def register():
    """Registration form."""
    if current_user.is_authenticated:
            return redirect(url_for('user', username=current_user.username, _external=True, _scheme='http'))

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

    staff_members = Staff.query.filter_by(user_id=current_user.id)
    if staff_members is None:
        staff_members = []

    form = StaffRegistrationForm(csfr_enable=False)

    if form.validate_on_submit():
        staff = Staff(
            name=form.staff_name.data,
            email=form.staff_email.data,
            role=form.role.data,
            user_id=current_user.id
        )
        db.session.add(staff)
        db.session.commit()
        flash("Account created!")
        return redirect(url_for('coaches', _external=True, _scheme='http'))

    return render_template('register-staff.html', title='RegisterStaff', staff_members=staff_members, template_form=form)

@app.route('/register/athlete', methods=["GET", "POST"])
@login_required
def register_athlete():
    """Athlete Registration Form."""

    athlete = Athlete.query.filter_by(user_id=current_user.id)
    teams = Team.query.filter_by(user_id=current_user.id)
    
    form = AthleteRegistrationForm(csfr_enable=False)
    if form.validate_on_submit():
        athlete = Athlete(
            name=form.name.data,
            date_of_birth=form.date_of_birth.data,
            student_id=form.student_id.data,
            position=form.position.data,
            user_id=current_user.id,
            team_id =form.team_id.data
            )

        db.session.add(athlete)
        db.session.commit()
        flash("Athlete Profile Created")
        return redirect('/athletes')
    return render_template("register-athlete.html", title="RegisterAthlete", teams=teams, athletes=athletes, template_form=form)

@app.route('/athletes/<team_name>')
@login_required
def athletes(team_name):
    team = Team.query.filter_by(team_name=team_name).first()
    
    athletes = Athlete.query.filter_by(team_id=team.id)
    
    return render_template('team-athletes.html', athletes=athletes)

@app.route('/athletes')
@login_required
def athletes_list():
    
    athletes = Athlete.query.filter_by(user_id=current_user.id)

    return render_template('athletes.html', athletes=athletes)

@app.route('/register/team', methods=["GET", "POST"])
@login_required
def register_team():
    """Team Registration Form."""

    teams = Team.query.filter_by(user_id=current_user.id)

    if teams is None:
        teams = []        

    form = TeamRegistrationForm(csfr_enable=False)

    if form.validate_on_submit():
        team = Team(
            team_name = form.team_name.data,
            user_id = current_user.id
        )
        db.session.add(team)
        db.session.commit()
        flash(f"{team.team_name} has been added to your Team Roster.")
        return redirect('/team')
    return render_template("register-team.html", title='Team', teams=teams, template_form=form)

@app.route('/team')
@login_required
def team():
    teams = Team.query.filter_by(user_id=current_user.id)
    
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
            next_page = request.args.get('next') #  user redirect to the page who is supposed to log in
            flash("Successfully Logged In!")
            return redirect(next_page) if next_page else redirect(url_for('user', username=user.username , _external=True, _scheme='http'))
        else:
            flash("Unsucessful Log In Attempt!")
            return redirect(url_for('login', _external=True, _scheme='http'))
    return render_template('login.html', template_form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("Successfully Logged Out!")
    return redirect(url_for('index'))

# Login_required routes
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    teams = Team.query.filter_by(user_id=user.id)

    return render_template('user.html', user=user, teams=teams)

@app.route('/coaches')
@login_required
def coaches():
    coach = User.query.filter_by(id=current_user.id)
    staff = Staff.query.filter_by(user_id=current_user.id)
    return render_template('coaches.html', coach=coach, staff=staff)

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
        return redirect(url_for('contact', _external=True, _scheme='http'))
        
    return render_template('contact.html', template_form=form)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404