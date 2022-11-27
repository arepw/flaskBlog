from flask import render_template, redirect, url_for, request
from app import app, db
from models import Upload
from flask_security import login_required, current_user
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def check_file_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.get('/profile')
@login_required
def user_profile():
    return render_template('profile.html')


@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file and check_file_extension(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_meta = Upload(filename=filename, owner_id=current_user.id)
            db.session.add(file_meta)
            db.session.commit()
            return render_template('upload.html', filename=filename)
        else:
            return redirect(request.url)
    return render_template('upload.html')


@app.route('/image/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename=f'uploads/{filename}'), code=301)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(403)
def page_forbidden(e):
    return render_template('403.html'), 403
