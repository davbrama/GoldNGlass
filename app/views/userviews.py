from app import app
from flask_login import current_user, login_user, logout_user
from flask import redirect, url_for, g, render_template, flash, request, Blueprint
from app.models import User
from app.auth import OAuthSignIn
from mongoengine import DoesNotExist
from flask.views import MethodView
from flask_babel import gettext as _

users = Blueprint('users', __name__, template_folder='templates')


class Login(MethodView):
    def get(self):
        if g.user is not None and g.user.is_authenticated:
            return redirect(url_for('index'))
        providers = [{'provider': provider, 'logo': app.config['OAUTH_PROVIDERS'][provider]['conf']['logo_normal']} for
                     provider
                     in app.config['OAUTH_PROVIDERS'].keys()]
        return render_template('users/login.html',
                               title=_('Sign In'),
                               providers=providers)


class Authorize(MethodView):
    def get(self, provider_name):
        if not current_user.is_anonymous:
            return redirect(url_for('index'))
        oauth = OAuthSignIn(provider_name=provider_name)
        return oauth.authorize()


class Callback(MethodView):
    def get(self, provider_name):
        if not current_user.is_anonymous:
            return redirect(url_for('index'))
        oauth = OAuthSignIn(provider_name=provider_name)
        logged_user = oauth.callback()
        if not logged_user:
            flash(_('Authentication failed.'))
            return redirect(url_for('index'))
        try:
            user = User.objects.get(email=logged_user['email'])
            user.avatar = logged_user['avatar']
            user.save()
        except DoesNotExist:
            user = User(**logged_user)
            user.save()
        login_user(user, remember=True)
        return redirect(request.args.get('next') or url_for('index'))


class Home(MethodView):
    def get(self, email):
        if g.user.is_anonymous:
            return redirect(url_for('index'))
        return render_template('users/user.html', user=User.objects(email=email)[0])


class Logout(MethodView):
    def get(self):
        logout_user()
        return redirect(url_for('index'))


users.add_url_rule('/login', view_func=Login.as_view('login'))
users.add_url_rule('/authorize/<provider_name>', view_func=Authorize.as_view('authorize'))
users.add_url_rule('/callback/<provider_name>', view_func=Callback.as_view('callback'))
users.add_url_rule('/user/<email>', view_func=Home.as_view('user'))
users.add_url_rule('/logout', view_func=Logout.as_view('logout'))
