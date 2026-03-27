from functools import wraps
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Procedure, Application, Reservation
from app.forms import ProcedureForm, AcceptApplicationForm
from app.matching import rank_applications, auto_manage_waitlist

college_bp = Blueprint("college", __name__, template_folder="../templates")


def college_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if current_user.role != "college":
            abort(403)
        return f(*args, **kwargs)
    return decorated


@college_bp.route("/dashboard")
@college_required
def dashboard():
    profile = current_user.college_profile
    procedures = profile.procedures.order_by(Procedure.created_at.desc()).all()

    pending_count = 0
    for proc in procedures:
        pending_count += Application.query.filter_by(
            procedure_id=proc.id, status="pending"
        ).count()

    upcoming_reservations = (
        Reservation.query.join(Application)
        .join(Procedure)
        .filter(
            Procedure.college_id == profile.id,
            Reservation.status == "confirmed",
        )
        .order_by(Reservation.scheduled_date.asc())
        .limit(10)
        .all()
    )

    return render_template(
        "college/dashboard.html",
        profile=profile,
        procedures=procedures,
        pending_count=pending_count,
        upcoming_reservations=upcoming_reservations,
    )


@college_bp.route("/procedures")
@college_required
def procedures():
    profile = current_user.college_profile
    procs = profile.procedures.order_by(Procedure.created_at.desc()).all()
    return render_template("college/procedures.html", procedures=procs)


@college_bp.route("/procedures/new", methods=["GET", "POST"])
@college_required
def new_procedure():
    form = ProcedureForm()
    form.category.choices = Procedure.CATEGORIES

    if form.validate_on_submit():
        profile = current_user.college_profile
        procedure = Procedure(
            college_id=profile.id,
            name=form.name.data,
            category=form.category.data,
            description=form.description.data,
            estimated_cost=form.estimated_cost.data,
            market_cost=form.market_cost.data,
            total_slots=form.total_slots.data,
            date_available=form.date_available.data,
            date_deadline=form.date_deadline.data,
            duration_minutes=form.duration_minutes.data or 60,
        )
        db.session.add(procedure)
        db.session.commit()
        flash("Procedure created successfully!", "success")
        return redirect(url_for("college.procedures"))

    return render_template("college/procedure_form.html", form=form, editing=False)


@college_bp.route("/procedures/<int:proc_id>/edit", methods=["GET", "POST"])
@college_required
def edit_procedure(proc_id):
    profile = current_user.college_profile
    procedure = Procedure.query.get_or_404(proc_id)
    if procedure.college_id != profile.id:
        abort(403)

    form = ProcedureForm(obj=procedure)
    form.category.choices = Procedure.CATEGORIES

    if form.validate_on_submit():
        form.populate_obj(procedure)
        db.session.commit()
        flash("Procedure updated.", "success")
        return redirect(url_for("college.procedures"))

    return render_template("college/procedure_form.html", form=form, editing=True, procedure=procedure)


@college_bp.route("/procedures/<int:proc_id>/toggle", methods=["POST"])
@college_required
def toggle_procedure(proc_id):
    profile = current_user.college_profile
    procedure = Procedure.query.get_or_404(proc_id)
    if procedure.college_id != profile.id:
        abort(403)

    procedure.is_active = not procedure.is_active
    db.session.commit()
    status = "activated" if procedure.is_active else "deactivated"
    flash(f"Procedure {status}.", "info")
    return redirect(url_for("college.procedures"))


@college_bp.route("/procedures/<int:proc_id>/applications")
@college_required
def view_applications(proc_id):
    profile = current_user.college_profile
    procedure = Procedure.query.get_or_404(proc_id)
    if procedure.college_id != profile.id:
        abort(403)

    ranked = rank_applications(proc_id)

    # Also get accepted/completed/rejected for history
    history = Application.query.filter(
        Application.procedure_id == proc_id,
        Application.status.in_(["accepted", "rejected", "completed"]),
    ).order_by(Application.responded_at.desc()).all()

    return render_template(
        "college/applications.html",
        procedure=procedure,
        ranked_applications=ranked,
        history=history,
    )


@college_bp.route("/application/<int:app_id>/accept", methods=["GET", "POST"])
@college_required
def accept_application(app_id):
    profile = current_user.college_profile
    application = Application.query.get_or_404(app_id)
    procedure = application.procedure

    if procedure.college_id != profile.id:
        abort(403)
    if application.status not in ("pending", "waitlisted"):
        flash("This application cannot be accepted.", "warning")
        return redirect(url_for("college.view_applications", proc_id=procedure.id))

    form = AcceptApplicationForm()

    if form.validate_on_submit():
        # Accept the application
        application.status = "accepted"
        application.responded_at = datetime.utcnow()
        application.college_notes = form.college_notes.data

        # Create reservation
        reservation = Reservation(
            application_id=application.id,
            scheduled_date=form.scheduled_date.data,
            scheduled_time=form.scheduled_time.data,
            confirmation_code=Reservation.generate_code(),
        )
        db.session.add(reservation)

        # Update slot count
        procedure.filled_slots += 1
        db.session.commit()

        auto_manage_waitlist(procedure.id)

        flash(
            f"Application accepted! Confirmation code: {reservation.confirmation_code}",
            "success",
        )
        return redirect(url_for("college.view_applications", proc_id=procedure.id))

    return render_template(
        "college/application_detail.html",
        application=application,
        procedure=procedure,
        form=form,
    )


@college_bp.route("/application/<int:app_id>/reject", methods=["POST"])
@college_required
def reject_application(app_id):
    profile = current_user.college_profile
    application = Application.query.get_or_404(app_id)
    procedure = application.procedure

    if procedure.college_id != profile.id:
        abort(403)

    application.status = "rejected"
    application.responded_at = datetime.utcnow()
    db.session.commit()

    flash("Application declined.", "info")
    return redirect(url_for("college.view_applications", proc_id=procedure.id))


@college_bp.route("/reservations")
@college_required
def reservations():
    profile = current_user.college_profile
    res = (
        Reservation.query.join(Application)
        .join(Procedure)
        .filter(Procedure.college_id == profile.id)
        .order_by(Reservation.scheduled_date.desc())
        .all()
    )
    return render_template("college/reservations.html", reservations=res)


@college_bp.route("/reservation/<int:res_id>/complete", methods=["POST"])
@college_required
def complete_reservation(res_id):
    profile = current_user.college_profile
    reservation = Reservation.query.get_or_404(res_id)
    procedure = reservation.application.procedure

    if procedure.college_id != profile.id:
        abort(403)

    reservation.status = "completed"
    reservation.application.status = "completed"
    db.session.commit()

    flash("Reservation marked as completed.", "success")
    return redirect(url_for("college.reservations"))


@college_bp.route("/reservation/<int:res_id>/cancel", methods=["POST"])
@college_required
def cancel_reservation(res_id):
    profile = current_user.college_profile
    reservation = Reservation.query.get_or_404(res_id)
    procedure = reservation.application.procedure

    if procedure.college_id != profile.id:
        abort(403)

    reservation.status = "cancelled"
    reservation.application.status = "cancelled"
    procedure.filled_slots = max(0, procedure.filled_slots - 1)
    db.session.commit()

    auto_manage_waitlist(procedure.id)

    flash("Reservation cancelled. Waitlisted patients may be promoted.", "info")
    return redirect(url_for("college.reservations"))
