from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Procedure, Application, Reservation
from app.forms import ApplicationForm
from app.matching import compute_priority_score, auto_manage_waitlist

patient_bp = Blueprint("patient", __name__, template_folder="../templates")


def patient_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if current_user.role != "patient":
            abort(403)
        return f(*args, **kwargs)
    return decorated


@patient_bp.route("/dashboard")
@patient_required
def dashboard():
    profile = current_user.patient_profile
    active_apps = Application.query.filter(
        Application.patient_id == profile.id,
        Application.status.in_(["pending", "waitlisted", "accepted"]),
    ).order_by(Application.applied_at.desc()).all()

    reservations = (
        Reservation.query.join(Application)
        .filter(
            Application.patient_id == profile.id,
            Reservation.status == "confirmed",
        )
        .order_by(Reservation.scheduled_date.asc())
        .all()
    )

    return render_template(
        "patient/dashboard.html",
        profile=profile,
        active_apps=active_apps,
        reservations=reservations,
    )


@patient_bp.route("/apply/<int:procedure_id>", methods=["GET", "POST"])
@patient_required
def apply(procedure_id):
    procedure = Procedure.query.get_or_404(procedure_id)
    profile = current_user.patient_profile

    if not procedure.is_open:
        flash("This procedure is no longer accepting applications.", "warning")
        return redirect(url_for("main.college_detail", college_id=procedure.college_id))

    # Check for existing application
    existing = Application.query.filter_by(
        patient_id=profile.id, procedure_id=procedure_id
    ).first()
    if existing:
        flash("You have already applied for this procedure.", "info")
        return redirect(url_for("patient.applications"))

    form = ApplicationForm()
    form.urgency.choices = Application.URGENCY_LEVELS

    if form.validate_on_submit():
        score = compute_priority_score(form.urgency.data)
        application = Application(
            patient_id=profile.id,
            procedure_id=procedure_id,
            urgency=form.urgency.data,
            urgency_description=form.urgency_description.data,
            notes_to_college=form.notes_to_college.data,
            priority_score=score,
        )
        db.session.add(application)
        db.session.commit()

        auto_manage_waitlist(procedure_id)

        flash("Application submitted! You'll see updates on your dashboard.", "success")
        return redirect(url_for("patient.dashboard"))

    return render_template(
        "patient/apply.html", form=form, procedure=procedure
    )


@patient_bp.route("/applications")
@patient_required
def applications():
    profile = current_user.patient_profile
    apps = (
        Application.query.filter_by(patient_id=profile.id)
        .order_by(Application.applied_at.desc())
        .all()
    )
    return render_template("patient/my_applications.html", applications=apps)


@patient_bp.route("/application/<int:app_id>/cancel", methods=["POST"])
@patient_required
def cancel_application(app_id):
    profile = current_user.patient_profile
    application = Application.query.get_or_404(app_id)

    if application.patient_id != profile.id:
        abort(403)

    if application.status not in ("pending", "waitlisted"):
        flash("This application cannot be cancelled.", "warning")
        return redirect(url_for("patient.applications"))

    application.status = "cancelled"
    db.session.commit()

    auto_manage_waitlist(application.procedure_id)

    flash("Application cancelled.", "info")
    return redirect(url_for("patient.applications"))


@patient_bp.route("/reservations")
@patient_required
def reservations():
    profile = current_user.patient_profile
    res = (
        Reservation.query.join(Application)
        .filter(Application.patient_id == profile.id)
        .order_by(Reservation.scheduled_date.desc())
        .all()
    )
    return render_template("patient/reservations.html", reservations=res)
