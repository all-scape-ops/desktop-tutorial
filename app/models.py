from datetime import datetime, date
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # "patient" or "college"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    patient_profile = db.relationship(
        "PatientProfile", backref="user", uselist=False, cascade="all, delete-orphan"
    )
    college_profile = db.relationship(
        "CollegeProfile", backref="user", uselist=False, cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class PatientProfile(db.Model):
    __tablename__ = "patient_profile"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    zip_code = db.Column(db.String(10), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    has_insurance = db.Column(db.Boolean, default=False)
    medical_notes = db.Column(db.Text)

    applications = db.relationship("Application", backref="patient", lazy="dynamic")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class CollegeProfile(db.Model):
    __tablename__ = "college_profile"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.String(300), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    phone = db.Column(db.String(20))
    website = db.Column(db.String(300))
    is_verified = db.Column(db.Boolean, default=False)

    procedures = db.relationship("Procedure", backref="college", lazy="dynamic")

    @property
    def full_address(self):
        return f"{self.address}, {self.city}, {self.state} {self.zip_code}"


class Procedure(db.Model):
    __tablename__ = "procedure"

    id = db.Column(db.Integer, primary_key=True)
    college_id = db.Column(
        db.Integer, db.ForeignKey("college_profile.id"), nullable=False
    )
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    estimated_cost = db.Column(db.Float, nullable=False)
    market_cost = db.Column(db.Float, nullable=True)
    total_slots = db.Column(db.Integer, nullable=False)
    filled_slots = db.Column(db.Integer, default=0)
    date_available = db.Column(db.Date, nullable=False)
    date_deadline = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, default=60)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship("Application", backref="procedure", lazy="dynamic")

    CATEGORIES = [
        ("general", "General / Cleaning"),
        ("restorative", "Restorative (Fillings, Crowns)"),
        ("orthodontic", "Orthodontic (Braces, Aligners)"),
        ("surgical", "Surgical (Extractions)"),
        ("emergency", "Emergency Care"),
        ("cosmetic", "Cosmetic"),
    ]

    @property
    def slots_available(self):
        return self.total_slots - self.filled_slots

    @property
    def is_full(self):
        return self.filled_slots >= self.total_slots

    @property
    def savings_percent(self):
        if self.market_cost and self.market_cost > 0:
            return round((1 - self.estimated_cost / self.market_cost) * 100)
        return 0

    @property
    def is_open(self):
        return self.is_active and not self.is_full and self.date_deadline >= date.today()


class Application(db.Model):
    __tablename__ = "application"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(
        db.Integer, db.ForeignKey("patient_profile.id"), nullable=False
    )
    procedure_id = db.Column(
        db.Integer, db.ForeignKey("procedure.id"), nullable=False
    )
    urgency = db.Column(db.String(20), nullable=False)
    urgency_description = db.Column(db.Text)
    status = db.Column(db.String(20), default="pending")
    priority_score = db.Column(db.Integer, nullable=False)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    responded_at = db.Column(db.DateTime, nullable=True)
    notes_to_college = db.Column(db.Text)
    college_notes = db.Column(db.Text)

    reservation = db.relationship(
        "Reservation", backref="application", uselist=False, cascade="all, delete-orphan"
    )

    __table_args__ = (
        db.UniqueConstraint("patient_id", "procedure_id", name="uq_patient_procedure"),
    )

    URGENCY_LEVELS = [
        ("emergency", "Emergency - Severe pain or trauma"),
        ("pain", "In Pain - Ongoing discomfort"),
        ("routine", "Routine - Preventive / checkup"),
    ]

    STATUS_LABELS = {
        "pending": "Pending Review",
        "accepted": "Accepted",
        "rejected": "Not Selected",
        "waitlisted": "Waitlisted",
        "completed": "Completed",
        "cancelled": "Cancelled",
    }

    @property
    def status_label(self):
        return self.STATUS_LABELS.get(self.status, self.status)


class Reservation(db.Model):
    __tablename__ = "reservation"

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(
        db.Integer, db.ForeignKey("application.id"), unique=True, nullable=False
    )
    scheduled_date = db.Column(db.Date, nullable=False)
    scheduled_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default="confirmed")
    confirmation_code = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def generate_code():
        import random
        import string
        chars = string.ascii_uppercase + string.digits
        return "DC-" + "".join(random.choices(chars, k=6))
