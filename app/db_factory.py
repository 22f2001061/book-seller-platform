from faker import Faker
import factory
from factory.alchemy import SQLAlchemyModelFactory
from app.models import User, Book, Category, BookRequest
from app.db import db
import random

fake = Faker("en_IN")


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session

    fname = factory.Faker("first_name")
    lname = factory.Faker("last_name")
    username = factory.Faker("user_name")
    password = factory.Faker("password")
    email = factory.LazyAttribute(lambda a: f"{a.fname}.{a.lname}@example.com")
    role = factory.Faker("random_element", elements=["admin", "seller", "buyer"])


class CategoryFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Category
        sqlalchemy_session = db.session

    name = factory.Faker("word")


class BookFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Book
        sqlalchemy_session = db.session

    title = factory.Faker("sentence", nb_words=3)
    content = factory.Faker("text")
    author = factory.Faker("name")
    thumbnail = "mario.jpg"
    category_id = factory.LazyFunction(
        lambda: random.choice(Category.query.with_entities(Category.id).all())[0]
    )


class BookRequestFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = BookRequest
        sqlalchemy_session = db.session

    book_id = factory.LazyFunction(
        lambda: random.choice(Book.query.with_entities(Book.id).all())[0]
    )
    user_id = factory.LazyFunction(
        lambda: random.choice(User.query.with_entities(User.id).all())[0]
    )
    date_requested = factory.LazyFunction(
        lambda: fake.date_between(start_date="-1y", end_date="today")
    )
    date_issued = factory.LazyFunction(
        lambda: (
            None
            if random.random() < 0.5
            else fake.date_between(start_date="-6m", end_date="today")
        )
    )
    date_returned = factory.LazyFunction(
        lambda: (
            None
            if random.random() < 0.7
            else fake.date_between(start_date="-3m", end_date="today")
        )
    )
    status = factory.Faker(
        "random_element",
        elements=["accepted", "rejected", "pending", "revoked", "returned"],
    )


def seed_data():
    for _ in range(10):
        user = UserFactory()
        db.session.add(user)

    for _ in range(5):
        category = CategoryFactory()
        db.session.add(category)

    db.session.commit()

    for _ in range(20):
        book = BookFactory()
        db.session.add(book)

    db.session.commit()

    for _ in range(30):
        book_request = BookRequestFactory()
        db.session.add(book_request)

    db.session.commit()
