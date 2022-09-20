from flask import render_template, redirect, url_for, request
from app import app
from models import Post, Tag


@app.route('/')
def index():
    search_query = request.args.get('q')
    if search_query:
        return redirect(url_for('posts.posts_list', q=search_query))
    return render_template('index.html')


@app.get('/profile')
def user_profile():
    return render_template('profile.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(403)
def page_forbidden(e):
    return render_template('403.html'), 403
