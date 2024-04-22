# FLASK SQLALCHEMY IMPORT
from flask_sqlalchemy import SQLAlchemy
# FLASK LOGIN IMPORT
from flask_login import UserMixin


# INITIALIZE DATABASE
db = SQLAlchemy()


# USERS TABLE
class User(UserMixin, db.Model):
    # TABLE NAME
    __tablename__ = "Users"
    # TABLE COLUMNS
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)


# PRODUCT TABLE
class Product(db.Model):
    # TABLE NAME
    __tablename__ = "Products"
    # TABLE COLUMNS
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    image = db.Column(db.String(250), nullable=False)
    price = db.Column(db.String(250), nullable=False)
