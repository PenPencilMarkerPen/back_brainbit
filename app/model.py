from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

    
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    @login.user_loader  
    def load_user(id):
        return User.query.get(int(id))
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def get_id(self):
        return str(self.id)
class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    state = db.Column(db.Integer, nullable=True)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_survey = db.Column(db.Integer)
    positive = db.Column(db.Integer, nullable=False)
    negative = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(50), nullable=False)


