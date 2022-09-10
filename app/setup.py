from app import db, user_datastore
from models import User, Post, Tag
''' Looks foolish but I need this. '''


def init_and_create_admin():
    db.create_all()
    print('Database successfully initialised.'
          '\nEnter password for admin user (email = admin@root.com)')
    password = input()
    admin_user = user_datastore.create_user(email='admin@root.com', password=password)
    db.session.add(admin_user)
    db.session.commit()
    admin_user = User.query.first()
    role = user_datastore.create_role(name='admin')
    db.session.add(role)
    db.session.commit()
    user_datastore.add_role_to_user(admin_user, role)
    db.session.commit()
    return print('Success!\nFor login use email "admin@test.com" and your password.')


def create_demo_post():
    post = Post(title='Demo post', body='Just demo post, nothing else here.')
    db.session.add(post)
    db.session.commit()
    tag = Tag(title='boring')
    db.session.add(tag)
    db.session.commit()
    post = Post.query.first()
    tag = Tag.query.first()
    post.tags.append(tag)
    db.session.add(post)
    db.session.commit()
    return print('Success!')


if __name__ == '__main__':
    print('Welcome to the blog setup.\nPress Enter to initialise database.')
    input()
    init_and_create_admin()
    print('Press Enter to exit the setup. Input "1" to create demo post.')
    option = input()
    if int(option) == 1:
        create_demo_post()
