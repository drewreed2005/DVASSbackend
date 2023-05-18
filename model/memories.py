""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the Post class to manage actions in 'posts' table,  with a relationship to 'users' table


# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class Memory(db.Model):
    __tablename__ = 'memory'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _username = db.Column(db.String(255), unique=False, nullable=False)
    _streak = db.Column(db.Integer, unique=True, nullable=False)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, username, streak):
        self._username = username
        self._streak = streak

    # a username getter method, extracts username from object
    @property
    def username(self):
        return self._username
    
    # a setter function, allows username to be updated after initial object creation
    @username.setter
    def username(self, username):
        self._username = username
    
    # a getter method, extracts streak from object
    @property
    def streak(self):
        return self._streak
    
    # a setter function, allows streak to be updated after initial object creation
    @streak.setter
    def streak(self, streak):
        self._streak = streak
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "username": self.username,
            "streak": self.streak
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, username, streak):
        """only updates values with length"""
        if len(username) > 0:
            self.username = username
        if streak > 0:
            self.streak = streak
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """

# Builds working data for testing
def initMemory():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        u1 = Memory(username="Mr. Cards", streak=5)
        u2 = Memory(username="Kard Kowntre", streak=10)
        u3 = Memory(username="Un Bea Table", streak=15)

        users = [u1, u2, u3]

        """Builds sample user/note(s) data"""
        for user in users:
            try:
                user.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {user.username}")
            