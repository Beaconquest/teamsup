from datetime import datetime
from flask_package import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    """User account model."""

    __tablname__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name: str = db.Column(db.String(16), index=True, unique=False)
    last_name: str = db.Column(db.String(16), index=True, unique=False)
    email: str = db.Column(db.String(60), index=True, unique=True)
    role: str = db.Column(db.String(25), index=True, unique=False)
    phone: int = db.Column(db.Integer)
    criminal_ab:str = db.Column(db.String(60))
    nccp_number: int = db.Column(db.Integer, index=True, unique=True)
    nbiaa_policy: str = db.Column(db.String) 
    joined = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    username = db.Column(db.String(140), index=True, unique=True)
    password_hash = db.Column(db.String(140))
    
    teams = db.relationship('Team', backref='user', lazy='dynamic')
    athletes = db.relationship('Athlete', backref='user', lazy='dynamic')
    
    def __repr__(self):
        return f"User(Name: {self.first_name} {self.last_name}, role: {self.role})"

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)
    
    def is_password_correct(self, password: str):
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def _generate_password_hash(password):
        return generate_password_hash(password)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(140), index=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    athletes = db.relationship('Athlete', backref='team', lazy='dynamic')

    def __repr__(self):
        return f"Team: {self.team_name}"

class Athlete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True, unique=False)
    email = db.Column(db.String(140), index=True, unique=True)
    date_of_birth = db.Column(db.String, index=True, unique=False)
    student_id = db.Column(db.Integer, index=True, unique=True)
    position = db.Column(db.Integer, index=True, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

    def __repr__(self):
        return f"Athlete Name: {self.name}"


class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True, unique=False)
    email = db.Column(db.String(140), index=True, unique=True)
    role = db.Column(db.String(140), index=True, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Staff Name: {self.name}"

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), index=True, unique=False)
    email = db.Column(db.String(140), index=True, unique=False)
    body = db.Column(db.String(250), index=True, unique=False)
    message_date = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
