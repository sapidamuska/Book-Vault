from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)

    role = db.Column(db.String(30), default="member")
    approved = db.Column(db.Boolean, default=False)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    language = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    available = db.Column(db.Boolean, default=True)


class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))

    borrow_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(days=60))
    return_date = db.Column(db.DateTime, nullable=True)

    fine = db.Column(db.Float, default=0)

    user = db.relationship("User")
    book = db.relationship("Book")


class Warning(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer)
    book_id = db.Column(db.Integer)

    message = db.Column(db.String(300))
    type = db.Column(db.String(50))  # reminder / overdue

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
