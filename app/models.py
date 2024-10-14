from app.db import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    role = db.Column(db.String)  # admin, seller, buyer


# class Customer
# class Professional


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String, nullable=False)
    # description = db.Column(db.String, nullable=True)
    content = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    # pages
    thumbnail = db.Column(db.String, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)


class BookRequest(db.Model):
    __tablename__ = "book_requests"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    date_requested = db.Column(db.Date, default=datetime.now())
    date_issued = db.Column(db.Date, nullable=True)
    date_returned = db.Column(db.Date, nullable=True)
    status = db.Column(
        db.String, default="pending"
    )  # accepted, rejected, pending, revoked, returned
