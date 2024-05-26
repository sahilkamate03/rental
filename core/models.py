# Write Models Here

import datetime
from core import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


from sqlalchemy import Enum


class Users(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Store hashed passwords
    role = db.Column(db.Enum("seller", "buyer", name="user_roles"), nullable=False)


class InterestedBuyers(db.Model):
    __tablename__ = "interested_buyers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    property_id = db.Column(db.Integer, db.ForeignKey("properties.id"), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(
        db.TIMESTAMP, nullable=False, default=db.func.current_timestamp()
    )


class Properties(db.Model):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    seller_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    place = db.Column(db.String(100), nullable=False)
    area = db.Column(db.Integer, nullable=False)
    number_of_bedrooms = db.Column(db.Integer, nullable=False)
    number_of_bathrooms = db.Column(db.Integer, nullable=False)
    nearby_hospitals = db.Column(db.Boolean, nullable=False)
    nearby_colleges = db.Column(db.Boolean, nullable=False)
    property_type = db.Column(db.String(50), nullable=False)
    furnishing_status = db.Column(
        db.Enum("furnished", "semi-furnished", "unfurnished", name="furnishing_status"),
        nullable=False,
    )
    facing = db.Column(db.String(100), nullable=True)
    water_supply = db.Column(db.String(100), nullable=True)
    gated_security = db.Column(db.Boolean, nullable=True)
    parking = db.Column(db.Boolean, nullable=True)
    posted_on = db.Column(db.Date, nullable=True)
    age_of_building = db.Column(db.Integer, nullable=True)
    balcony = db.Column(db.Boolean, nullable=True)
    rent = db.Column(db.Integer, nullable=True)
    deposit = db.Column(db.Integer, nullable=True)


class Likes(db.Model):
    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    property_id = db.Column(db.Integer, db.ForeignKey("properties.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(
        db.TIMESTAMP, nullable=False, default=db.func.current_timestamp()
    )
