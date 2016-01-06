__author__ = 'Serban Carlogea'

from app import db
import datetime
from app.models.user import User
from app.utils import get_bookmark

class Bookmark(db.Document):
    user = db.ReferenceField(User, required=True)
    url = db.StringField(required=True)
    title = db.StringField()
    description = db.StringField()
    content = db.StringField()
    screenshot = db.StringField(default=None)
    public = db.BooleanField(default=False)
    tags = db.ListField(db.StringField())
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    updated_at = db.DateTimeField(required=False)
    deleted_at = db.DateTimeField(default=None, required=False)

    meta = {
        'ordering': ['-updated_at', '-created_at']
    }

    def save(self, *args, **kwargs):

        if self.updated_at is None:
            bookmark = get_bookmark(self)
            self.url = bookmark.url
            self.title = bookmark.title
            self.description = bookmark.description
            self.tags = bookmark.tags

        self.updated_at = datetime.datetime.now()
        return super(Bookmark, self).save(*args, **kwargs)

    def to_dict(self):
        return {
            'id': str(self.id),
            'url': self.url,
            'title': self.title,
            'description': self.description,
            'screenshot': self.screenshot,
            'tags': self.tags if self.tags else [],
            'user': str(self.user.id) if self.user else None,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at) if self.updated_at else None
        }
