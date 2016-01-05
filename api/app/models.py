__author__ = 'Serban Carlogea'

from app import app, db
import datetime
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import extraction
import requests


class User(db.Document):
    email = db.StringField(required=True, max_length=255)
    password_hash = db.StringField(max_length=255)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    updated_at = db.DateTimeField(default=datetime.datetime.now, required=True)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    @staticmethod
    def generate_auth_token(email, password, expiration=86400):
        user = User.objects(email=email).first()
        if user and user.verify_password(password):
            s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
            return s.dumps({'id': str(user.id)})
        return None


class Bookmark(db.Document):
    user = db.ReferenceField(User, required=True)
    url = db.StringField(required=True)
    title = db.StringField()
    description = db.StringField()
    public = db.BooleanField(default=False)
    tags = db.ListField(db.StringField())
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    updated_at = db.DateTimeField(required=False)

    meta = {
        'ordering': ['-updated_at', '-created_at']
    }

    def fetch(self):
        html = requests.get(self.url).text
        if html:
            extracted = extraction.Extractor().extract(html, source_url=self.url)
            self.title = extracted.title
            self.description = extracted.description
            self.updated_at = datetime.datetime.now
            return True
        return False

    def to_dict(self):
        return {
            'id': str(self.id),
            'url': self.url,
            'title': self.title,
            'description': self.description,
            'tags': self.tags if self.tags else ['Video', 'Web page', 'Article', 'News'],
            'user': str(self.user.id) if self.user else None,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at) if self.updated_at else None
        }
