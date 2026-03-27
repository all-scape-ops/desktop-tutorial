"""
Priority matching engine for DentalConnect.

Patients are ranked by:
1. Health urgency tier (emergency > pain > routine)
2. First-come-first-served within the same tier
"""

from datetime import datetime
from app.models import Application, Procedure
from app.extensions import db

URGENCY_WEIGHTS = {
    "emergency": 1000,
    "pain": 500,
    "routine": 100,
}


def compute_priority_score(urgency, applied_at=None):
    """Compute a priority score. Higher = higher priority.

    Within the same urgency tier, earlier applications get a small bonus
    (up to 99 points), so first-come-first-served is the tiebreaker.
    """
    base = URGENCY_WEIGHTS.get(urgency, 100)

    if applied_at:
        hours_elapsed = (datetime.utcnow() - applied_at).total_seconds() / 3600
        time_bonus = max(0, 99 - int(hours_elapsed))
    else:
        time_bonus = 99  # Just submitted

    return base + time_bonus


def rank_applications(procedure_id):
    """Return all pending/waitlisted applications for a procedure, ranked by priority."""
    applications = (
        Application.query.filter(
            Application.procedure_id == procedure_id,
            Application.status.in_(["pending", "waitlisted"]),
        )
        .order_by(Application.priority_score.desc(), Application.applied_at.asc())
        .all()
    )
    return applications


def auto_manage_waitlist(procedure_id):
    """When slots fill up, waitlist remaining. When slots open, promote from waitlist."""
    procedure = Procedure.query.get(procedure_id)
    if not procedure:
        return

    if procedure.is_full:
        # Waitlist all remaining pending applications
        pending = Application.query.filter_by(
            procedure_id=procedure_id, status="pending"
        ).all()
        for app in pending:
            app.status = "waitlisted"
        db.session.commit()
    else:
        # Promote from waitlist if slots opened up
        slots_open = procedure.slots_available
        if slots_open > 0:
            waitlisted = (
                Application.query.filter_by(
                    procedure_id=procedure_id, status="waitlisted"
                )
                .order_by(
                    Application.priority_score.desc(), Application.applied_at.asc()
                )
                .limit(slots_open)
                .all()
            )
            for app in waitlisted:
                app.status = "pending"
            db.session.commit()
