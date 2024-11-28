from flask import Flask
from routes import auth, files
from app import create_app
import os



flask_app = create_app() 


# Run the Flask app
if __name__ == '__main__':
    flask_app.run(debug=True)

