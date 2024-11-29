from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete="CASCADE"), nullable=False)  # Ensure role_id is NOT NULL
    role = db.relationship('Role', backref=db.backref('users', lazy=True))

    def set_password(self, password):
        """Set hashed password"""
        self.password = generate_password_hash(password)

    def set_role(self, role_name='USER'):
        """Assign a role to the user (default to 'USER')"""
        role = Role.query.filter_by(name=role_name).first()
        if role:
            self.role = role
        else:
            raise ValueError(f"Role '{role_name}' does not exist")

    def check_password(self, password):
        """Check password hash"""
        return check_password_hash(self.password, password)

    def has_role(self, role_name):
        """Check if user has a specific role"""
        return self.role.name == role_name if self.role else False

    def __repr__(self):
        return f"User {self.username} with role {self.role.name if self.role else 'No role'}"

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return f"Role {self.name}"

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())