from sqlalchemy import (
    create_engine, Column, Integer, String, Text,
    ForeignKey
)
from sqlalchemy.orm import (
    scoped_session, sessionmaker, relationship, backref
)
from sqlalchemy.ext.declarative import declarative_base

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound

import bcrypt

db_engine = None
db_session = scoped_session(sessionmaker(autoflush=True))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    Base.metadata.create_all(bind=db_engine)

def clear_db():
    Base.metadata.drop_all(bind=db_engine)

def initialise_engine(db_uri):
    global db_engine
    db_engine = create_engine(db_uri, convert_unicode=True)
    db_session.configure(bind=db_engine)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    email = Column(String(100), unique=True)
    password = Column(String())

    def __init__(self, username, email, plaintext):
        self.username = username
        self.email = email
        self.password = self.generate_bcrypt_hash(plaintext)

    def generate_bcrypt_hash(self, plaintext):
        return bcrypt.hashpw(plaintext, bcrypt.gensalt())

    def check_bcrypt_hash(self, plaintext):
        return bcrypt.hashpw(plaintext, self.password) == self.password

class Snippet(Base):
    __tablename__ = 'snippets'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    snippet_lang = Column(String(30))
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship("User", backref=backref('snippets', order_by=id))
    snippet_raw = Column(Text())
    snippet_formatted = Column(Text())

    def __init__(self, title, snippet_lang, author, snippet_raw):
        self.title = title
        self.snippet_lang = snippet_lang
        self.author = author
        self.snippet_raw = snippet_raw
        self.snippet_formatted = self.generate_formatted()

    def generate_formatted(self):
        lexer = None
        try:
            lexer = get_lexer_by_name(self.snippet_lang.lower())
        except ClassNotFound:
            lexer = get_lexer_by_name('text')
        formatter = HtmlFormatter(linenos=True, cssclass='source')
        return highlight(self.snippet_raw, lexer, formatter)
