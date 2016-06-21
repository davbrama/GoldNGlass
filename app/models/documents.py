import datetime
from flask import url_for, g
from app import db
from .users import User


class Comment(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.datetime.utcnow(), required=True)
    body = db.StringField(verbose_name="Comment", required=True)
    author = db.ReferenceField(User)


class Post(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.utcnow(), required=True)
    title = db.StringField(max_length=255, required=True)
    slug = db.StringField(max_length=255, required=True)
    comments = db.ListField(db.EmbeddedDocumentField('Comment'))
    tags = db.ListField(db.StringField(max_length=32))
    body = db.StringField(required=True)

    def get_absolute_url(self):
        return url_for('post', kwargs={"slug": self.slug})

    def __unicode__(self):
        return self.title

    @classmethod
    def get_all_tags(cls):
        taglist = set()
        for post_tags in cls.objects.only('tags'):
            taglist = taglist | set(post_tags.tags)
        return taglist

    @property
    def post_type(self):
        return self.__class__.__name__

    meta = {
        'allow_inheritance': True,
        'indexes': [
            {'fields': ['$title', "$body", "$tags"],
             'default_language': 'english',
             'weights': {'title': 10, 'tags': 6, 'body': 2}
             },
            '-created_at', 'slug'],
        'ordering': ['-created_at']
    }
