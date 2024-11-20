from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for, session
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# Secret key for session management (you should change this to a more secure key)
app.secret_key = 'your_secret_key'

# Directory to store uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configure the upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Dummy users (this should be replaced with a database in production)
users = {'admin': 'password123'}

# Route to serve the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            session['user'] = username  # Store username in session to keep user logged in
            return redirect(url_for('home'))  # Redirect to the main page (dashboard)
        else:
            return 'Invalid credentials, please try again.'  # Error message on failed login

    return render_template('login.html')  # Render the login page for GET requests

# Route to serve the frontend (NAS Dashboard)
@app.route('/')
def home():
    if 'user' not in session:  # Check if the user is logged in
        return redirect(url_for('login'))  # Redirect to login page if not logged in
    return render_template('index.html')  # Serve the NAS dashboard page

# Route to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the file to the upload folder
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    return jsonify({'message': 'File uploaded successfully!'})

# Route to list uploaded files
@app.route('/files', methods=['GET'])
def list_files():
    try:
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        return jsonify(files)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to download a file
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        # Force download by setting Content-Disposition header
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to logout
@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove the user from the session
    return redirect(url_for('login'))  # Redirect to login page

if __name__ == '__main__':
    app.run(debug=True)
