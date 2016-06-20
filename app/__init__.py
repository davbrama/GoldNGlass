from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object('config')


db = MongoEngine(app)
lm = LoginManager()


def register_blueprints(app):
    from app.views import docviews, posts
    from app.models import User, Post, Comment
    app.register_blueprint(posts)


register_blueprints(app)
lm.init_app(app)
lm.login_view = 'login'

if __name__ == '__main__':
    app.run()
