from flask import Blueprint, render_template, request
from app.models import CollegeProfile, Procedure
from app.forms import SearchForm
from app.geo import find_colleges_nearby
from datetime import date

main_bp = Blueprint("main", __name__, template_folder="../templates")


@main_bp.route("/")
def index():
    # Show stats on landing page
    total_colleges = CollegeProfile.query.count()
    active_procedures = Procedure.query.filter(
        Procedure.is_active == True,
        Procedure.date_deadline >= date.today(),
    ).count()
    return render_template(
        "index.html",
        total_colleges=total_colleges,
        active_procedures=active_procedures,
    )


@main_bp.route("/search")
def search():
    form = SearchForm(request.args)
    form.category.choices = [("", "All Procedures")] + Procedure.CATEGORIES

    results = []
    searched = False

    if request.args.get("zip_code"):
        searched = True
        zip_code = request.args.get("zip_code", "").strip()
        radius = int(request.args.get("radius", 50))
        category = request.args.get("category", "")

        # Get all colleges with active procedures
        query = CollegeProfile.query
        colleges = query.all()

        # Filter by distance
        nearby = find_colleges_nearby(colleges, zip_code, radius)

        # Build results with procedure counts
        for college, distance in nearby:
            proc_query = college.procedures.filter(
                Procedure.is_active == True,
                Procedure.date_deadline >= date.today(),
            )
            if category:
                proc_query = proc_query.filter(Procedure.category == category)

            procedures = proc_query.all()
            if procedures:
                results.append({
                    "college": college,
                    "distance": distance,
                    "procedures": procedures,
                    "procedure_count": len(procedures),
                })

    return render_template("patient/search.html", form=form, results=results, searched=searched)


@main_bp.route("/college/<int:college_id>")
def college_detail(college_id):
    college = CollegeProfile.query.get_or_404(college_id)
    procedures = college.procedures.filter(
        Procedure.is_active == True,
        Procedure.date_deadline >= date.today(),
    ).order_by(Procedure.date_deadline.asc()).all()

    return render_template(
        "patient/college_detail.html",
        college=college,
        procedures=procedures,
    )
