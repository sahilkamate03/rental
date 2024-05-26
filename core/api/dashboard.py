from datetime import datetime
import random
from flask import Blueprint, render_template, jsonify

from core.models import Properties, Users
from core import db

dashboard = Blueprint("dashboard", __name__)


def add_dummy_data():
    # Add users
    # BEGIN: ed8c6549bwf9
    for _ in range(9):
        user = Users.query.filter_by(email=f"user{{_}}@example.com").first()
        if not user:
            user = Users(
                name="User{}".format(_),
                email="user{}@example.com".format(_),
                phone_number="1234567890",
                password="password",
                role=random.choice(["seller", "buyer"]),
            )
            db.session.add(user)
    db.session.commit()
    # END: ed8c6549bwf9

    # Add properties
    # BEGIN: be15d9bcejpp
    for _ in range(30):
        property = Properties.query.filter_by(title="Property{}".format(_)).first()
        if not property:
            property = Properties(
                seller_id=random.randint(1, 9),
                title="Property{}".format(_),
                description="Description for Property{}".format(_),
                place="Location{}".format(_),
                area=random.randint(500, 2000),
                number_of_bedrooms=random.randint(1, 5),
                number_of_bathrooms=random.randint(1, 3),
                nearby_hospitals=random.choice([True, False]),
                nearby_colleges=random.choice([True, False]),
                property_type=random.choice(["Apartment", "House", "Villa"]),
                furnishing_status=random.choice(
                    ["furnished", "semi-furnished", "unfurnished"]
                ),
                facing=random.choice(["North", "South", "East", "West"]),
                water_supply=random.choice(["Corporation", "Borewell", "Tanker"]),
                gated_security=random.choice([True, False]),
                parking=random.choice([True, False]),
                posted_on=datetime.now(),
                age_of_building=random.randint(1, 20),
                balcony=random.choice([True, False]),
                rent=random.randint(5000, 20000),
                deposit=random.randint(10000, 50000),
            )
            db.session.add(property)
    db.session.commit()
    # END: be15d9bcejpp
    for _ in range(10):
        user = Users(
            name="User{}".format(_),
            email="user{}@example.com".format(_),
            phone_number="1234567890",
            password="password",
            role=random.choice(["seller", "buyer"]),
        )
        db.session.add(user)
    db.session.commit()

    # Add properties
    for _ in range(30):
        property = Properties(
            seller_id=random.randint(1, 10),
            title="Property{}".format(_),
            description="Description for Property{}".format(_),
            place="Location{}".format(_),
            area=random.randint(500, 2000),
            number_of_bedrooms=random.randint(1, 5),
            number_of_bathrooms=random.randint(1, 3),
            nearby_hospitals=random.choice([True, False]),
            nearby_colleges=random.choice([True, False]),
            property_type=random.choice(["Apartment", "House", "Villa"]),
            furnishing_status=random.choice(
                ["furnished", "semi-furnished", "unfurnished"]
            ),
            facing=random.choice(["North", "South", "East", "West"]),
            water_supply=random.choice(["Corporation", "Borewell", "Tanker"]),
            gated_security=random.choice([True, False]),
            parking=random.choice([True, False]),
            posted_on=datetime.now(),
            age_of_building=random.randint(1, 20),
            balcony=random.choice([True, False]),
            rent=random.randint(5000, 20000),
            deposit=random.randint(10000, 50000),
        )
        db.session.add(property)

    db.session.commit()
