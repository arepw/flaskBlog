from flask import render_template, redirect, url_for, request
from app import app
from models import Post, Tag
from flask_security import login_required


@app.route('/')
def index():
    return render_template('index.html')


@app.get('/profile')
@login_required
def user_profile():
    return render_template('profile.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(403)
def page_forbidden(e):
    return render_template('403.html'), 403
