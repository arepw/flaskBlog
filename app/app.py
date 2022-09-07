from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)  # Takes config class as an argument for configuration


db = SQLAlchemy(app)

migrate = Migrate(app, db, compare_type=True)
