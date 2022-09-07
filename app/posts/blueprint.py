from flask import Blueprint, render_template, request
from models import Post, Tag

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/')
def posts_list():
    search_query = request.args.get('q')
    if search_query:
        all_posts = Post.query.filter(Post.title.contains(search_query) |
                                      Post.body.contains(search_query)
                                      )
    else:
        all_posts = Post.query.all()
    return render_template('posts/posts.html', posts=all_posts)


@posts.route('/<slug>')
def post_details(slug):
    post = Post.query.filter(Post.slug == slug).first()
    return render_template('posts/post_detail.html', post=post)


@posts.route('/tags/<slug>')
def tag_details(slug):
    tag = Tag.query.filter(Tag.slug == slug).first()
    return render_template('posts/tag_detail.html', tag=tag)
