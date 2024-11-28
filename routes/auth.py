from flask import flash,Blueprint,request, render_template, redirect, url_for, session
from flask_login import current_user, login_required, login_user
from model import User
from app import db

auth = Blueprint('auth', __name__,
                        template_folder='../templates')




# Secret key for session management

# Dummy user authentication (replace with real user management in production)
# users = {'admin': 'password123'}


# Route to login page
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template('register.html',error="User already exists")
        else:
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
            session['role'] = user.role
            return redirect(url_for('auth.home'))  # Redirect to homepage after login
            # login_user(user)
            # return redirect(url_for('auth.home'))
            
        else:
            flash('Invalid credentials, please try again.', 'error')  # Flash error message
            return redirect(url_for('auth.login')) 
    
    return render_template('login.html')  # Render login page for GET requests

# Route to home/dashboard page
@auth.route('/')
def home():
    if 'user' not in session:  # If no user is logged in, redirect to login
        return redirect(url_for('auth.login'))
    
    return render_template('index.html')  # Render the main page (NAS dashboard)

# Route to logout
@auth.route('/logout')
def logout():
    session.pop('user', None)  # Remove user from session
    return redirect(url_for('auth.login'))  # Redirect to login page




@auth.route('/metrics')
def metrics():
    if 'role' not in session or session['role'] != 'ADMIN':
        # Redirect to another template if the role is not ADMIN
        return render_template('403.html')  # Custom template for access denied

    return render_template('metrics.html')  # Render the main page (NAS dashboard)


