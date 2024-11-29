from flask import flash,Blueprint,request, render_template, redirect, url_for,current_app, session, jsonify
from flask_principal import Identity, identity_changed, AnonymousIdentity
from flask_login import current_user, login_required, login_user, logout_user
from model import User
from app import db

auth = Blueprint('auth', __name__,
                        template_folder='../templates')



# Route to login page
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template('register.html',error="User already exists")
        
        new_user =User(username=username)
        new_user.set_password(password)
        new_user.set_role("USER")
        db.session.add(new_user)
        db.session.commit()
        session['username']= username
        return redirect(url_for('auth.home'))  # Redirect to homepage after login
       
    
    return render_template('register.html')  # Render Register page for GET requests


# Route to login page
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user'] = username  # Store user in session
            session['role'] = user.role.name if user.role else 'USER'
            # return redirect(url_for('auth.home'))  # Redirect to homepage after login
            login_user(user)
            # Inform Flask-Principal about the user's roles
            identity = Identity(user.id)
            identity_changed.send(current_app._get_current_object(), identity=identity)
            return redirect(url_for('auth.home'))
            
        else:
            flash('Invalid credentials, please try again.', 'error')  # Flash error message
            return redirect(url_for('auth.login')) 
    
    return render_template('login.html')  # Render login page for GET requests
   

# Route to home/dashboard page
@auth.route('/')
@login_required
def home():
    if 'user' not in session:  # If no user is logged in, redirect to login
        return redirect(url_for('auth.login'))
    
    return render_template('index.html')  # Render the main page (NAS dashboard)

# Route to logout
@auth.route('/logout')
@login_required
def logout():
    if current_user.is_authenticated:
        # Log the user out
        logout_user()
        
        # Inform Flask-Principal of the logout event
        identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
        session.pop('user', None)  # Remove user from session
        session.pop('role', None)  # Remove user from session
        return redirect(url_for('auth.login'))  # Redirect to login page
    return jsonify({"error": "No user is logged in"}), 400




@auth.route('/metrics')
def metrics():
    if 'role' not in session or session['role'] != 'ADMIN':
        # Redirect to another template if the role is not ADMIN
        return render_template('403.html')  # Custom template for access denied

    return render_template('metrics.html')  # Render the main page (NAS dashboard)


