import datetime
from app import db


class User(db.Document):
    email = db.EmailField(required=True, unique=True, primary_key=True)
    nickname = db.StringField(required=True)
    fullname = db.StringField()
    avatar = db.URLField()
    last_seen = db.DateTimeField(default=datetime.datetime.utcnow(), required=True)
    active = db.BooleanField(default=True)
    admin = db.BooleanField(default=False)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email

    def __repr__(self):
        return '<User %r>' % self.nickname

