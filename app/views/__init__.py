from .docviews import posts
from .userviews import *
from app import app, lm
from flask import g
from datetime import datetime
from flask_login import current_user
from app.models import User


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