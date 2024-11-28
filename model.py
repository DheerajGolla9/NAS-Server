from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.Text, nullable=False)


    def set_password(self,password):
        self.password = generate_password_hash(password)

    def set_role(self,role):
        self.role = role

    def check_password(self,password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'Preson with name {self.username} and age {self.password}'
