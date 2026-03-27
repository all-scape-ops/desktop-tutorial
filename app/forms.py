from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, TextAreaField, SelectField,
    FloatField, IntegerField, DateField, BooleanField, TimeField,
)
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length, NumberRange, Optional, ValidationError,
)
from app.models import User


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])


class PatientRegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    first_name = StringField("First Name", validators=[DataRequired(), Length(max=80)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(max=80)])
    phone = StringField("Phone", validators=[Optional(), Length(max=20)])
    date_of_birth = DateField("Date of Birth", validators=[Optional()])
    zip_code = StringField("Zip Code", validators=[DataRequired(), Length(min=5, max=10)])
    medical_notes = TextAreaField("Medical Notes / Conditions", validators=[Optional()])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError("An account with this email already exists.")


class CollegeRegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    name = StringField("College / School Name", validators=[DataRequired(), Length(max=200)])
    description = TextAreaField("About Your Program", validators=[Optional()])
    address = StringField("Street Address", validators=[DataRequired(), Length(max=300)])
    city = StringField("City", validators=[DataRequired(), Length(max=100)])
    state = StringField("State (2-letter)", validators=[DataRequired(), Length(min=2, max=2)])
    zip_code = StringField("Zip Code", validators=[DataRequired(), Length(min=5, max=10)])
    phone = StringField("Phone", validators=[Optional(), Length(max=20)])
    website = StringField("Website", validators=[Optional(), Length(max=300)])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError("An account with this email already exists.")


class ProcedureForm(FlaskForm):
    name = StringField("Procedure Name", validators=[DataRequired(), Length(max=200)])
    category = SelectField("Category", validators=[DataRequired()], choices=[])
    description = TextAreaField("Description", validators=[Optional()])
    estimated_cost = FloatField(
        "Patient Cost ($)", validators=[DataRequired(), NumberRange(min=0)]
    )
    market_cost = FloatField("Market Price ($)", validators=[Optional(), NumberRange(min=0)])
    total_slots = IntegerField(
        "Available Slots", validators=[DataRequired(), NumberRange(min=1)]
    )
    date_available = DateField("Available From", validators=[DataRequired()])
    date_deadline = DateField("Application Deadline", validators=[DataRequired()])
    duration_minutes = IntegerField(
        "Duration (minutes)", validators=[Optional(), NumberRange(min=15)]
    )


class ApplicationForm(FlaskForm):
    urgency = SelectField("Urgency Level", validators=[DataRequired()], choices=[])
    urgency_description = TextAreaField(
        "Describe Your Situation", validators=[DataRequired(), Length(max=1000)]
    )
    notes_to_college = TextAreaField(
        "Additional Notes for the College", validators=[Optional(), Length(max=500)]
    )


class AcceptApplicationForm(FlaskForm):
    scheduled_date = DateField("Appointment Date", validators=[DataRequired()])
    scheduled_time = TimeField("Appointment Time", validators=[DataRequired()])
    college_notes = TextAreaField("Internal Notes", validators=[Optional()])


class SearchForm(FlaskForm):
    class Meta:
        csrf = False  # GET form, no CSRF needed

    zip_code = StringField("Zip Code", validators=[Optional()])
    category = SelectField("Procedure Type", validators=[Optional()], choices=[])
    radius = SelectField(
        "Distance",
        choices=[
            ("25", "25 miles"),
            ("50", "50 miles"),
            ("100", "100 miles"),
            ("250", "250 miles"),
        ],
        default="50",
    )
