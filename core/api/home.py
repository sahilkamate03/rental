from flask import Blueprint, render_template, url_for, redirect, request, flash, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from core.forms import UserForm, LoginForm, RegistrationForm
from core.models import InterestedBuyers, Users, Properties
from core import db
from sqlalchemy import inspect, func


home = Blueprint("home", __name__)


@home.route("/")
@login_required
def homes():
    user_data = current_user
    user_dict = {
        c.key: getattr(user_data, c.key) for c in inspect(user_data).mapper.column_attrs
    }
    page = request.args.get("page", 1, type=int)
    num = request.args.get("num", 0, type=int)
    if num == 1:
        properties_data = Properties.query.filter_by(
            furnishing_status="furnished"
        ).paginate(page=page, per_page=9)
        flash("Furnished Properties", "info")
    elif num == 2:
        properties_data = Properties.query.filter_by(parking=True).paginate(
            page=page, per_page=9
        )
        flash("Parking Properties", "info")
    elif num == 3:
        properties_data = Properties.query.filter_by(balcony=True).paginate(
            page=page, per_page=9
        )
        flash("Balcony Properties", "info")

    else:
        properties_data = Properties.query.paginate(page=page, per_page=9)
        flash("All Properties", "info")

    # Add the count of interested users to each property
    for property in properties_data.items:
        count = (
            db.session.query(func.count(InterestedBuyers.id))
            .filter(InterestedBuyers.property_id == property.id)
            .scalar()
        )
        property.like = count
    return render_template(
        "home.html", user_data=user_dict, properties_data=properties_data
    )


@home.route("/signin", methods=["GET", "POST"])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for("home.homes"))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        input_password = form.password.data

        try:
            user = Users.query.filter_by(email=email).first()
            if user is None:
                flash("User not found. Create Account.", "info")
                return redirect(url_for("home.signup"))

            if input_password != user.password:
                flash("Login Unsuccessful. Please check email and password", "danger")
                return redirect(url_for("home.signin"))

            next_page = request.args.get("next")
            login_user(user, remember=form.remember.data)
            return redirect(next_page) if next_page else redirect(url_for("home.homes"))
        except Exception as e:
            flash("Login Unsuccessful. Please check email and password", "danger")
            print(e)
            return redirect(url_for("home.signin"))

    return render_template("./signin.html", title="Login", form=form)


@home.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("home.homes"))
    form = RegistrationForm()
    if form.validate_on_submit():
        print("success")
        email = form.email.data
        password = form.password.data
        role = form.role.data
        data = {
            "name": form.name.data,
            "email": email,
            "phone_number": form.phone_number.data,
            "password": password,
            "role": role,
        }

        print(data)
        try:
            user = Users(**data)
            db.session.add(user)
            db.session.commit()

            flash(f"User Registered.", "info")
            return redirect(url_for("home.signin"))
        except Exception as e:
            print(e)

    return render_template("./signup.html", title="Register", form=form)


@home.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home.signin"))


@home.route("/api")
def home_latest():
    return jsonify({"message": "Hello Server"})
