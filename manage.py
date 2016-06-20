#!/usr/bin/env python
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_script import Manager, Server
from app import app
from config import DEBUG
from app.models import User

manager = Manager(app)
manager.add_command("runserver", Server(
    use_debugger=DEBUG,
    use_reloader=DEBUG,
    host='0.0.0.0'))


@manager.command
def grantadmin(email):
    user = User.objects(email=email)[0]
    user.admin = True
    user.save()


@manager.command
def revokeadmin(email):
    user = User.objects(email=email)[0]
    user.admin = False
    user.save()


if __name__ == "__main__":
    manager.run()
