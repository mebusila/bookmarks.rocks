__author__ = 'Serban Carlogea'

from app import db
from passlib.apps import custom_app_context as pwd_context
import datetime


class User(db.Document):
    email = db.StringField(required=True, max_length=255)
    password_hash = db.StringField(max_length=255)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    updated_at = db.DateTimeField(default=datetime.datetime.now, required=True)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def to_dict(self):
        return {
            'id': str(self.id),
            'email': str(self.email)
        }