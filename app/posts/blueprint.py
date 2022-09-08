from flask import Blueprint, render_template, request, redirect, url_for
from models import Post, Tag
from app import db
from .forms import PostForm

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/create', methods=['POST', 'GET'])
def post_create():
    form = PostForm()
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')

        try:
            post = Post(title=title, body=body)
            db.session.add(post)
            db.session.commit()
        except:  # TODO: Use "except" properly
            print('Something went completely wrong')
        return redirect(url_for('posts.post_details', slug=post.slug))

    return render_template('posts/post_create.html', form=form)


@posts.route('/')
def posts_list():
    search_query = request.args.get('q')
    if search_query:
        all_posts = Post.query.filter(Post.title.contains(search_query) |
                                      Post.body.contains(search_query)
                                      )
    else:
        all_posts = Post.query.order_by(Post.created.desc())

    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    pages = all_posts.paginate(page=page, per_page=3)
    return render_template('posts/posts.html', posts=all_posts, pages=pages)


@posts.route('/<slug>')
def post_details(slug):
    post = Post.query.filter(Post.slug == slug).first()
    return render_template('posts/post_detail.html', post=post)


@posts.route('/tags/<slug>')
def tag_details(slug):
    tag = Tag.query.filter(Tag.slug == slug).first()
    return render_template('posts/tag_detail.html', tag=tag)


@posts.route('/<slug>/edit', methods=['POST', 'GET'])
def post_update(slug):
    post = Post.query.filter(Post.slug == slug).first()
    if request.method == 'POST':
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()
        return redirect(url_for('posts.post_details', slug=post.slug))
    form = PostForm(obj=post)
    return render_template('posts/edit.html', post=post, form=form)
