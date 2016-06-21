from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_babel import Babel
from flask_misaka import Misaka

md = Misaka()
app = Flask(__name__)
app.config.from_object('config')


db = MongoEngine(app)
lm = LoginManager()
babel = Babel(app)
md.init_app(app)

def register_blueprints(app):
    from app.views import docviews, posts, users, admin
    from app.models import User, Post, Comment
    app.register_blueprint(posts)
    app.register_blueprint(users)
    app.register_blueprint(admin)


register_blueprints(app)
lm.init_app(app)
lm.login_view = 'users.login'


if __name__ == '__main__':
    app.run()
