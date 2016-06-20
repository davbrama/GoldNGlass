from app import app
from flask_login import current_user, login_user, logout_user
from flask import redirect, url_for, g, render_template, flash, request
from app.models import User
from app.auth import OAuthSignIn
from mongoengine import DoesNotExist


@app.route('/authorize/<provider_name>')
def authorize(provider_name):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn(provider_name=provider_name)
    return oauth.authorize()


@app.route('/callback/<provider_name>')
def callback(provider_name):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn(provider_name=provider_name)
    resp = oauth.callback()
    if not resp:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    params = app.config['OAUTH_PROVIDERS'][provider_name]['params']
    logged_user = {}
    for key in params.keys():
        logged_user[key] = eval('resp'+params[key])
    try:
        user = User.objects.get(email=logged_user['email'])
    except DoesNotExist:
        user = User(**logged_user)
        user.save()
    login_user(user, remember=True)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/login')
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    providers = [{'provider': provider, 'logo': app.config['OAUTH_PROVIDERS'][provider]['conf']['logo_normal']} for provider
                 in app.config['OAUTH_PROVIDERS'].keys()]
    return render_template('users/login.html',
                           title='Sign In',
                           providers=providers)


@app.route('/user/<email>')
def user(email):
    if g.user.is_anonymous:
        return redirect(url_for('index'))
    return render_template('users/user.html', user=User.objects(email=email)[0])


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

