from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_security import SQLAlchemyUserDatastore, Security, current_user
from flask_mailman import Mail

app = Flask(__name__)
app.config.from_object(Config)  # Takes config class as an argument for configuration

db = SQLAlchemy(app)
from models import *

migrate = Migrate(app, db, compare_type=True)
mail = Mail(app)


# Flask-Admin
# TODO: Flask-Admin to separate .py file
class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class AdminView(AdminMixin, ModelView):
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    pass


class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        if is_created:
            model.generate_slug()
        if type(model) is Post:
            model.generate_short()
        return super().on_model_change(form, model, is_created)


class PostAdminView(AdminMixin, BaseModelView):
    form_columns = ['title', 'body', 'tags']


class TagAdminView(AdminMixin, BaseModelView):
    form_columns = ['title', 'posts']


admin = Admin(app, 'Flask Blog', url='/', template_mode='bootstrap4', index_view=HomeAdminView(name='Admin'))
admin.add_view(PostAdminView(Post, db.session))
admin.add_view(TagAdminView(Tag, db.session))

# Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
