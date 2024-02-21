"""
This file (test_models.py) contains the unit tests for the models.py file.
"""
from flask_package.models import User
from werkzeug.security import generate_password_hash

def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the first name, last name , username, hashed_passowrd, and role fields are defined correctly
    """

    user = User(first_name='Promise', last_name='Mwenga', role='coach', username='test1', password_hash=generate_password_hash('test1', method='sha256'))
    assert user.first_name == 'Promise'
    assert user.last_name == 'Mwenga'
    assert user.username == 'test1'
    assert user.password_hash != 'test1'
    assert user.role == 'coach'