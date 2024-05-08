from flask import Flask
from config import Config

# Initialize Flask application with configurations from the Config class
app = Flask(__name__)
app.config.from_object(Config)

# Import the web module to set up routes and views
from app import web