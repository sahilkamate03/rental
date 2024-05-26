# Write Forms Here
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    TextAreaField,
    RadioField,
    SelectField,
    IntegerField,
    DecimalField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
    InputRequired,
    NumberRange,
)
from core.models import Users


class UserForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), Length(max=50)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(max=50)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=100)])
    phone_number = StringField(
        "Phone Number", validators=[DataRequired(), Length(max=15)]
    )
    password = PasswordField("Password", validators=[DataRequired(), Length(max=255)])
    role = SelectField(
        "Role",
        choices=[("seller", "Seller"), ("buyer", "Buyer")],
        validators=[DataRequired()],
    )


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")

    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])

    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    phone_number = StringField(
        "Phone Number", validators=[DataRequired(), Length(max=15)]
    )
    role = SelectField(
        "Role",
        choices=[("buyer", "Buyer"), ("seller", "Seller")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Create Account")

    def validate_email(self, email):
        try:
            user = Users.query.filter_by(
                email=email.data
            ).first()  # Query the user by email
        except Exception as e:
            user = False

        if user:
            raise ValidationError("That email is taken. Please choose a different one.")

        if "@" in email.data:
            ait = email.data.split("@")[1]
        else:
            raise ValidationError("Enter valid email.")


class PropertyForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=100)])
    description = TextAreaField("Description", validators=[DataRequired()])
    place = StringField("Place", validators=[DataRequired(), Length(max=100)])
    area = IntegerField(
        "Area",
        validators=[
            DataRequired(),
            NumberRange(min=1, message="Area must be a positive integer."),
        ],
    )
    number_of_bedrooms = IntegerField(
        "Number of Bedrooms",
        validators=[
            DataRequired(),
            NumberRange(min=1, message="Number of bedrooms must be at least 1."),
        ],
    )
    number_of_bathrooms = IntegerField(
        "Number of Bathrooms",
        validators=[
            DataRequired(),
            NumberRange(min=1, message="Number of bathrooms must be at least 1."),
        ],
    )
    nearby_hospitals = BooleanField("Nearby Hospitals")
    nearby_colleges = BooleanField("Nearby Colleges")
    property_type = StringField(
        "Property Type", validators=[DataRequired(), Length(max=50)]
    )
    furnishing_status = SelectField(
        "Furnishing Status",
        choices=[
            ("furnished", "Furnished"),
            ("semi-furnished", "Semi-Furnished"),
            ("unfurnished", "Unfurnished"),
        ],
        validators=[DataRequired()],
    )
    facing = SelectField(
        "Facing",
        choices=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
            ("northeast", "Northeast"),
            ("northwest", "Northwest"),
            ("southeast", "Southeast"),
            ("southwest", "Southwest"),
        ],
    )
    water_supply = StringField("Water Supply", validators=[Length(max=100)])
    gated_security = BooleanField("Gated Security")
    parking = BooleanField("Parking")
    age_of_building = IntegerField(
        "Age of Building",
        validators=[
            NumberRange(
                min=0, message="Age of building must be a non-negative integer."
            )
        ],
    )
    balcony = BooleanField("Balcony")
    rent = IntegerField(
        "Rent",
        validators=[NumberRange(min=0, message="Rent must be a non-negative integer.")],
    )
    deposit = IntegerField(
        "Deposit",
        validators=[
            NumberRange(min=0, message="Deposit must be a non-negative integer.")
        ],
    )
    submit = SubmitField("Submit")
