from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models import User, PatientProfile, CollegeProfile
from app.forms import LoginForm, PatientRegistrationForm, CollegeRegistrationForm
from app.geo import get_coordinates

auth_bp = Blueprint("auth", __name__, template_folder="../templates")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return _redirect_dashboard()

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Welcome back!", "success")
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            return _redirect_dashboard()
        flash("Invalid email or password.", "danger")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/register/patient", methods=["GET", "POST"])
def register_patient():
    if current_user.is_authenticated:
        return _redirect_dashboard()

    form = PatientRegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data.lower(), role="patient")
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()  # Get user.id

        coords = get_coordinates(form.zip_code.data)
        profile = PatientProfile(
            user_id=user.id,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data,
            date_of_birth=form.date_of_birth.data,
            zip_code=form.zip_code.data,
            latitude=coords[0] if coords else None,
            longitude=coords[1] if coords else None,
            has_insurance=False,
            medical_notes=form.medical_notes.data,
        )
        db.session.add(profile)
        db.session.commit()

        login_user(user)
        flash("Account created! Welcome to DentalConnect.", "success")
        return redirect(url_for("patient.dashboard"))

    return render_template("auth/register_patient.html", form=form)


@auth_bp.route("/register/college", methods=["GET", "POST"])
def register_college():
    if current_user.is_authenticated:
        return _redirect_dashboard()

    form = CollegeRegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data.lower(), role="college")
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()

        coords = get_coordinates(form.zip_code.data)
        profile = CollegeProfile(
            user_id=user.id,
            name=form.name.data,
            description=form.description.data,
            address=form.address.data,
            city=form.city.data,
            state=form.state.data.upper(),
            zip_code=form.zip_code.data,
            latitude=coords[0] if coords else None,
            longitude=coords[1] if coords else None,
            phone=form.phone.data,
            website=form.website.data,
        )
        db.session.add(profile)
        db.session.commit()

        login_user(user)
        flash("College registered! Welcome to DentalConnect.", "success")
        return redirect(url_for("college.dashboard"))

    return render_template("auth/register_college.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.index"))


def _redirect_dashboard():
    if current_user.role == "patient":
        return redirect(url_for("patient.dashboard"))
    return redirect(url_for("college.dashboard"))
