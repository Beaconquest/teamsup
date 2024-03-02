"""
This file (test_models.py) contains the unit tests for the models.py file.
"""
from flask_package.models import User, Athlete, Team
from werkzeug.security import generate_password_hash

def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the first name, last name , username, hashed_passowrd, and role fields are defined correctly
    """

    user = User(id=1, first_name='Promise', last_name='Mwenga', role='coach', username='test1', password_hash=generate_password_hash('test1'))
    assert user.first_name == 'Promise'
    assert user.last_name == 'Mwenga'
    assert user.username == 'test1'
    assert user.password_hash != 'test1'
    assert user.role == 'coach'


def test_new_team():
    """
    GIVEN a Team model
    WHEN a new Team is created
    THEN check the team name, user id
    """

    team = Team(id=1, team_name="Black Kats", user_id=1)
    assert team.team_name == "Black Kats"
    assert team.user_id == 1

def test_new_athlete():
    """
    GIVEN a Athlete Model
    WHEN a new Athlete is created
    THEN check the first name, last name, student number
    """

    athlete = Athlete(id=1, first_name="Leo", last_name="Mwenga", student_id=235467,
                      team_id=1)
    assert athlete.first_name == 'Leo'
    assert athlete.last_name == 'Mwenga'
    assert athlete.student_id == 235467