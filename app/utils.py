from functools import wraps
from flask_login import current_user, current_app
from flask import request


def admin_required(func):

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method == 'OPTIONS':
            return func(*args, **kwargs)
        elif current_app.login_manager._login_disabled:
            return func(*args, **kwargs)
        elif current_user.is_anonymous:
            return current_app.login_manager.unauthorized()
        elif not current_user.admin:
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view
