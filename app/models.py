from app import db
from time import time
import re
from flask_security import UserMixin, RoleMixin
from textwrap import shorten


def slugify(s):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', s)


post_tags = db.Table('posts_tags',
                     db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                     )

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
                       )


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    short = db.Column(db.String(100))
    body = db.Column(db.Text)
    created = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    tags = db.relationship('Tag', secondary=post_tags,
                           backref=db.backref('posts'), lazy='dynamic'
                           )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_slug()
        self.generate_short()

    def generate_slug(self):
        """
        Makes the post title usable for url
        """
        # User can try to create a new post with the title == other post's slug.
        # This will cause integrity error. So, to prevent it from happening,
        # we must make sure that the DB don't already have Post with that slug.
        if self.title and self.query.where(Post.slug == self.title).first() is None:
            self.slug = slugify(self.title)
        else:
            self.slug = str(int(time()))

    def generate_short(self):
        self.short = shorten(self.body, width=100, placeholder="...")

    def __repr__(self):
        return f'<Post id: {self.id}, title: {self.title}>'


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        """
        Makes the tag title usable for url
        """
        if self.title and self.query.where(Tag.slug == self.title).first() is None:
            self.slug = slugify(self.title)
        else:
            self.slug = str(int(time()))

    def __repr__(self):
        return f'<Tag id: {self.id}, title: {self.title}>'


class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(120), unique=True, index=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    fs_uniquifier = db.Column(db.String(255), unique=True)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users')
                            )
    confirmed_at = db.Column(db.DateTime(timezone=True))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
