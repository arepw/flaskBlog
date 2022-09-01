from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config


app = Flask(__name__)
app.config.from_object(Config)  # Takes config class as an argument for configuration


db = SQLAlchemy(app)
