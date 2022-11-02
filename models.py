


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
        return f"Date register: {self.joined_at_date}, Role: {self.role}, Name: {self.name}, Username: {self.username}, Email: {self.email}"

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