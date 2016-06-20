#!/usr/bin/env python
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_script import Manager, Server
from app import app
from config import DEBUG

manager = Manager(app)
manager.add_command("runserver", Server(
    use_debugger=DEBUG,
    use_reloader=DEBUG,
    host='0.0.0.0'))

if __name__ == "__main__":
    manager.run()
