import os
from datetime import datetime

from app import db
from app import filesystem
from app.utils import get_random_string


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    dropbox_id = db.Column(db.Integer)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120))
    emailer = db.Column(db.String(120), unique=True)
    added_bookmarklet = db.Column(db.Boolean)
    uploaded_welcome_pdf = db.Column(db.Boolean)
    active = db.Column(db.Boolean)
    access_token = db.Column(db.Text)
    cursor = db.Column(db.Text)

    # @kindle.com email addresses.
    kindle_names = db.relationship('KindleName', backref='user', lazy='dynamic',
                                   cascade='delete')
    # Hashes of the user's current books.
    books = db.relationship('Book', backref='user', lazy='dynamic',
                            cascade='delete')

    def __init__(self, dropbox_id):
        self.dropbox_id = dropbox_id
        self.added_bookmarklet = False
        self.uploaded_welcome_pdf = False
        self.active = False

    def set_active(self, active):
        self.active = active

    def set_new_emailer(self):
        random_base = get_random_string()
        emailer_address = 'mailer+%s@mail.getbookdrop.com' % random_base
        self.emailer = emailer_address
        return random_base

    def set_added_bookmarklet(self):
        self.added_bookmarklet = True

    def set_uploaded_welcome_pdf(self):
        self.uploaded_welcome_pdf = True


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    book_hash = db.Column(db.Text)
    pathname = db.Column(db.Text)
    size = db.Column(db.Integer)
    unsent = db.Column(db.Boolean)
    num_attempts = db.Column(db.Integer)
    date_created = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, user_id, pathname, size, unsent=False, book_hash=''):
        self.user_id = user_id
        self.pathname = pathname
        self.book_hash = book_hash
        self.size = size
        # Books are always unsent at first
        self.mark_unsent(True)
        self.num_attempts = 0
        if self.date_created is None:
            self.date_created = datetime.utcnow()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<Book: {0}>".format(self.pathname)


    def mark_unsent(self, unsent):
        self.unsent = unsent

    def get_size(self):
        if self.size is None:
            return 0
        else:
            return self.size

    def get_tmp_pathname(self, tag):
        return os.path.join(filesystem.get_user_directory(self.user_id, tag),
                            self.pathname.strip('/'))


class KindleName(db.Model):
    __tablename__ = 'kindle_name'
    id = db.Column(db.Integer, primary_key=True)
    kindle_name = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, user_id, kindle_name):
      self.user_id = user_id
      self.kindle_name = kindle_name

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<KindleName: {0}>".format(self.kindle_name)
