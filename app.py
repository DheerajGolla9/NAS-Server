from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from werkzeug.security import generate_password_hash



db=SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dheeraj.db'  # Update with your database path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

     # Create the default admin user within the app context
    with app.app_context():
        create_default_admin_user()


    from route import register_routes
    register_routes(app,db)

    migrate = Migrate(app,db)


    return app


def create_default_admin_user():
    from model import User
    """Check if the 'admin' user exists, if not, create one."""
    # Try to find the 'admin' user
    admin_user = User.query.filter_by(username='admin').first()
    
    if not admin_user:
        # If the 'admin' user does not exist, create it
        hashed_password = generate_password_hash('adminpassword')  # Set a secure password
        admin_user = User(username='admin', password=hashed_password, role='ADMIN')  # Assuming you have a 'role' field in your model
        db.session.add(admin_user)
        db.session.commit()
        print("Default admin user created.")

