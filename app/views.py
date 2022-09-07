from flask import render_template
from app import app
from models import Post, Tag


@app.route('/')
def index():
    return render_template('index.html')
