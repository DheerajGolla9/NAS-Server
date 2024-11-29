from flask import Flask
from routes import auth, files, users
from model import User
import os


app = Flask(__name__)



# Folder for uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)



def register_routes(app, db):
    
    app.secret_key = 'samplejkahfddh'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # app.register_blueprint(files)
    app.register_blueprint(auth)
    app.register_blueprint(files)
    app.register_blueprint(users)

