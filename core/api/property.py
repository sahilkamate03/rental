from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
from flask import Blueprint, flash, jsonify, request, render_template
from flask_login import current_user, login_user, logout_user, login_required
import requests
from sqlalchemy import inspect
from core.models import Properties, Users, db, InterestedBuyers
from core.forms import LoginForm, PropertyForm
from datetime import datetime
from flask import redirect, url_for
from flask import redirect, url_for
from flask import redirect, url_for

property = Blueprint("property", __name__)


@property.route("/add_property_details", methods=["POST"])
@login_required
def add_property_details():
    if not current_user.is_authenticated:
        return redirect(url_for("home.signin"))

    form = PropertyForm()
    if form.validate_on_submit():
        property_data = Properties(
            seller_id=current_user.get_id(),  # Get the user ID from current_user
            title=form.title.data,
            description=form.description.data,
            place=form.place.data,
            area=form.area.data,
            number_of_bedrooms=form.number_of_bedrooms.data,
            number_of_bathrooms=form.number_of_bathrooms.data,
            nearby_hospitals=form.nearby_hospitals.data,
            nearby_colleges=form.nearby_colleges.data,
            property_type=form.property_type.data,
            furnishing_status=form.furnishing_status.data,
            facing=form.facing.data,
            water_supply=form.water_supply.data,
            gated_security=form.gated_security.data,
            parking=form.parking.data,
            posted_on=datetime.now(),
            age_of_building=form.age_of_building.data,
            balcony=form.balcony.data,
            rent=form.rent.data,
            deposit=form.deposit.data,
        )
        # print(current_user.get_id())
        db.session.add(property_data)
        db.session.commit()
    else:
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                print(f"Error in {fieldName}: {err}")

    return jsonify({"message": "Property details added successfully"})


@property.route("/property_form")
@login_required
def property_form():
    if not current_user.is_authenticated:
        return redirect(url_for("home.signin"))

    user_data = current_user
    user_dict = {
        c.key: getattr(user_data, c.key) for c in inspect(user_data).mapper.column_attrs
    }
    print(user_dict)
    form = PropertyForm()
    return render_template("property_form.html", user_data=user_dict, form=form)


@property.route("/property_delete/<int:property_id>")
@login_required
def property_delete(property_id):
    if not current_user.is_authenticated:
        return redirect(url_for("home.signin"))

    property = Properties.query.filter_by(id=property_id).first()
    db.session.delete(property)
    db.session.commit()
    flash("Property deleted successfully", "success")
    return redirect(url_for("profile.account"))


@property.route("/update_property_form/<int:property_id>")
@login_required
def update_property_form(property_id):
    if not current_user.is_authenticated:
        return redirect(url_for("home.signin"))

    user_data = current_user
    user_dict = {
        c.key: getattr(user_data, c.key) for c in inspect(user_data).mapper.column_attrs
    }
    form = PropertyForm()
    return render_template(
        "update_property_form.html",
        property_id=property_id,
        user_data=user_dict,
        form=form,
    )


@property.route("/update_property_details/<int:property_id>", methods=["POST"])
@login_required
def update_property_details(property_id):
    if  not current_user.is_authenticated:
        return redirect(url_for("home.signin"))

    form = PropertyForm()
    if form.validate_on_submit():
        property = Properties.query.filter_by(id=property_id).first()
        property.title = form.title.data
        property.description = form.description.data
        property.place = form.place.data
        property.area = form.area.data
        property.number_of_bedrooms = form.number_of_bedrooms.data
        property.number_of_bathrooms = form.number_of_bathrooms.data
        property.nearby_hospitals = form.nearby_hospitals.data
        property.nearby_colleges = form.nearby_colleges.data
        property.property_type = form.property_type.data
        property.furnishing_status = form.furnishing_status.data
        property.facing = form.facing.data
        property.water_supply = form.water_supply.data
        property.gated_security = form.gated_security.data
        property.parking = form.parking.data
        property.age_of_building = form.age_of_building.data
        property.balcony = form.balcony.data
        property.rent = form.rent.data
        property.deposit = form.deposit.data
        db.session.commit()
        return redirect(url_for("home.homes"))
    else:
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                print(f"Error in {fieldName}: {err}")

    return jsonify({"message": "Property details updated successfully"})


@property.route("/property/detail/<int:property_id>")
@login_required
def property_detail(property_id):
    if not current_user.is_authenticated:
        return redirect(url_for("home.signin"))
    user_data = current_user
    user_dict = {
        c.key: getattr(user_data, c.key) for c in inspect(user_data).mapper.column_attrs
    }
    property_data = Properties.query.filter_by(id=property_id).first()

    img_src = requests.get("https://picsum.photos/500")
    # property_data.img_src = img_src.url
    property_dict = {
        c.key: getattr(property_data, c.key)
        for c in inspect(property_data).mapper.column_attrs
    }

    property_dict["img_src"] = img_src.url
    return render_template(
        "property_detail.html", p_dict=property_dict, user_data=user_dict
    )


@property.route("/property_like/<int:property_id>")
@login_required
def property_like(property_id):
    if not current_user.is_authenticated:
        return redirect(url_for("home.signin"))
    user_id = current_user.id
    ib = InterestedBuyers(property_id=property_id, buyer_id=user_id)
    db.session.add(ib)
    db.session.commit()
    return redirect(url_for("home.homes"))


def send_email(email, content):
    sender = os.getenv("EMAIL")
    recipient = email
    subject = "PropertyGuru "

    body = f"""
    Hello {email.split('@')[0]},
    {content}

    Thanks
    """

    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = os.getenv("EMAIL")
    smtp_password = os.getenv("EMAIL_PWD")

    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(smtp_username, smtp_password)
        smtp.sendmail(sender, recipient, message.as_string())


@property.route("/intrested/<int:property_id>")
@login_required
def isIntrested(property_id):
    if  not current_user.is_authenticated:
        return redirect(url_for("home.signin"))

    user_id = current_user.id
    user_email = current_user.email
    property_data = Properties.query.filter_by(id=property_id).first()
    seller_id = property_data.seller_id
    seller_data = Users.query.filter_by(id=seller_id).first()
    seller_email = seller_data.email
    send_email(
        seller_email,
        content=f"User with email {user_email} is intrested in your property",
    )
    send_email(
        user_email,
        content=f"Your intrest in the property has been sent to the seller. You will be contacted soon. Seller email: {seller_email}",
    )
    # return {"user_id": user_id, "user_email": user_email, "seller_email": seller_email}
    flash("Intrested in property mail sent.", "success")
    return redirect(url_for("property.property_detail", property_id=property_id))
