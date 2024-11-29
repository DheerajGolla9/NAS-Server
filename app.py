from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from werkzeug.security import generate_password_hash
from flask_principal import Principal, Permission, RoleNeed,identity_loaded,UserNeed



login_manager = LoginManager()
principal = Principal()

# Define roles
admin_permission = Permission(RoleNeed('ADMIN'))
user_permission = Permission(RoleNeed('USER'))


# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from model import User
    return User.query.get(user_id) 



db=SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nasvarun.db'  # Update with your database path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

     
    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Specify your login route
    
    # Initialize Flask-Principal
    principal.init_app(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        # Set the user object for the identity
        if current_user.is_authenticated:
            identity.user = current_user

            # Add the user's id (UserNeed) to the identity
            identity.provides.add(UserNeed(current_user.id))

            # Add the user's role (RoleNeed) to the identity
            if current_user.role:  # Assuming the user has a `role` attribute
                identity.provides.add(RoleNeed(current_user.role.name))

    #Create the default admin user within the app context
    #with app.app_context():
    #    create_default_data()



    from route import register_routes
    register_routes(app,db)

    migrate = Migrate(app,db)


    return app



def create_default_data():
    from model import User
    """Create default roles and the default admin user if not exists."""
    # Seed roles
    seed_roles()

    # Create the default admin user if it doesn't exist
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        hashed_password = generate_password_hash('adminpassword')  # Replace with a secure password
        admin_user = User(username='admin', password=hashed_password)
        
        # Assign the 'ADMIN' role to the new user
        assign_role_to_user(admin_user, 'ADMIN')
        
        db.session.add(admin_user)
        db.session.commit()
        print("Default admin user created.")
    else:
        print("Admin user already exists.")



def assign_role_to_user(user, role_name):
    from model import Role
    """Assign a role to a user."""
    role = Role.query.filter_by(name=role_name).first()

    if role:
        user.role = role  # Assign the role directly
        db.session.commit()
        print(f"Role '{role_name}' assigned to user '{user.username}'.")
    else:
        print(f"Role '{role_name}' not found.")



def seed_roles():
    from model import Role
    """Seed roles into the database."""
    # Check if the roles already exist, if not, create them
    admin_role = Role.query.filter_by(name='ADMIN').first()
    user_role = Role.query.filter_by(name='USER').first()

    if not admin_role:
        admin_role = Role(name='ADMIN')
        db.session.add(admin_role)

    if not user_role:
        user_role = Role(name='USER')
        db.session.add(user_role)

    db.session.commit()
    print("Roles seeded successfully.")
