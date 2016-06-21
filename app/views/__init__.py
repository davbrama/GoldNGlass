from .docviews import posts
from .userviews import users
from .admin import admin
from app import app, lm, babel
from flask import g, redirect, url_for, request
from datetime import datetime
from flask_login import current_user
from app.models import User


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        g.user.save()


@lm.user_loader
def load_user(email):
    return User.objects.get(email=email)


@app.route('/index')
def index():
    return redirect(url_for('posts.list'))