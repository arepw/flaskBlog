from flask import render_template, redirect, url_for, request
from app import app
from models import Post, Tag


@app.route('/')
def index():
    search_query = request.args.get('q')
    if search_query:
        return redirect(url_for('posts.posts_list', q=search_query))
    return render_template('index.html')
