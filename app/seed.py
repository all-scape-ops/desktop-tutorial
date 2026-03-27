"""Seed data for DentalConnect demo."""

from datetime import date, timedelta
from app.extensions import db
from app.models import User, PatientProfile, CollegeProfile, Procedure
from app.geo import get_coordinates


def register_seed_command(app):
    @app.cli.command("seed")
    def seed():
        """Populate database with sample data."""
        _seed_data()
        print("Database seeded successfully!")


def _seed_data():
    # Don't seed twice
    if CollegeProfile.query.first():
        print("Data already exists, skipping seed.")
        return

    colleges = [
        {
            "email": "admin@nyudental.example.com",
            "password": "demo123",
            "name": "NYU College of Dentistry",
            "description": "One of the largest dental schools in the US, offering comprehensive patient care at reduced costs under expert supervision.",
            "address": "345 E 24th St",
            "city": "New York",
            "state": "NY",
            "zip_code": "10010",
            "phone": "(212) 998-9800",
            "website": "https://dental.nyu.edu",
        },
        {
            "email": "admin@columbia-dental.example.com",
            "password": "demo123",
            "name": "Columbia University College of Dental Medicine",
            "description": "Training the next generation of dental professionals while serving the community with affordable oral health care.",
            "address": "630 W 168th St",
            "city": "New York",
            "state": "NY",
            "zip_code": "10032",
            "phone": "(212) 305-6100",
            "website": "https://dental.columbia.edu",
        },
        {
            "email": "admin@upenn-dental.example.com",
            "password": "demo123",
            "name": "Penn Dental Medicine",
            "description": "University of Pennsylvania's dental school providing patient care in a teaching environment with state-of-the-art facilities.",
            "address": "240 S 40th St",
            "city": "Philadelphia",
            "state": "PA",
            "zip_code": "19104",
            "phone": "(215) 898-8965",
            "website": "https://dental.upenn.edu",
        },
        {
            "email": "admin@ucsf-dental.example.com",
            "password": "demo123",
            "name": "UCSF School of Dentistry",
            "description": "Leading dental school on the West Coast, offering patient care through student clinics at significantly reduced fees.",
            "address": "707 Parnassus Ave",
            "city": "San Francisco",
            "state": "CA",
            "zip_code": "94143",
            "phone": "(415) 476-1891",
            "website": "https://dentistry.ucsf.edu",
        },
        {
            "email": "admin@umich-dental.example.com",
            "password": "demo123",
            "name": "University of Michigan School of Dentistry",
            "description": "Top-ranked dental school providing excellent patient care through supervised student clinics.",
            "address": "1011 N University Ave",
            "city": "Ann Arbor",
            "state": "MI",
            "zip_code": "48109",
            "phone": "(734) 763-6933",
            "website": "https://dent.umich.edu",
        },
        {
            "email": "admin@uth-dental.example.com",
            "password": "demo123",
            "name": "UTHealth Houston School of Dentistry",
            "description": "Texas's premier dental school offering comprehensive care at reduced costs in the heart of the medical center.",
            "address": "7500 Cambridge St",
            "city": "Houston",
            "state": "TX",
            "zip_code": "77030",
            "phone": "(713) 486-4000",
            "website": "https://dentistry.uth.edu",
        },
    ]

    for c in colleges:
        user = User(email=c["email"], role="college")
        user.set_password(c["password"])
        db.session.add(user)
        db.session.flush()

        coords = get_coordinates(c["zip_code"])
        profile = CollegeProfile(
            user_id=user.id,
            name=c["name"],
            description=c["description"],
            address=c["address"],
            city=c["city"],
            state=c["state"].upper(),
            zip_code=c["zip_code"],
            latitude=coords[0] if coords else None,
            longitude=coords[1] if coords else None,
            phone=c["phone"],
            website=c["website"],
            is_verified=True,
        )
        db.session.add(profile)
        db.session.flush()

        # Add procedures for each college
        today = date.today()
        procedures = [
            {
                "name": "Teeth Cleaning (Prophylaxis)",
                "category": "general",
                "description": "Professional teeth cleaning including scaling, polishing, and oral hygiene education.",
                "estimated_cost": 25,
                "market_cost": 150,
                "total_slots": 20,
                "date_available": today,
                "date_deadline": today + timedelta(days=60),
                "duration_minutes": 60,
            },
            {
                "name": "Dental Exam & X-Rays",
                "category": "general",
                "description": "Comprehensive oral exam with digital X-rays and treatment planning consultation.",
                "estimated_cost": 15,
                "market_cost": 200,
                "total_slots": 25,
                "date_available": today,
                "date_deadline": today + timedelta(days=45),
                "duration_minutes": 45,
            },
            {
                "name": "Composite Filling",
                "category": "restorative",
                "description": "Tooth-colored filling for cavities. Includes local anesthesia and composite restoration.",
                "estimated_cost": 50,
                "market_cost": 300,
                "total_slots": 15,
                "date_available": today,
                "date_deadline": today + timedelta(days=30),
                "duration_minutes": 90,
            },
            {
                "name": "Root Canal Treatment",
                "category": "restorative",
                "description": "Endodontic treatment to save an infected tooth. Performed under close faculty supervision.",
                "estimated_cost": 150,
                "market_cost": 1200,
                "total_slots": 8,
                "date_available": today,
                "date_deadline": today + timedelta(days=45),
                "duration_minutes": 120,
            },
            {
                "name": "Simple Tooth Extraction",
                "category": "surgical",
                "description": "Non-surgical extraction of a tooth. Includes local anesthesia and post-op care instructions.",
                "estimated_cost": 40,
                "market_cost": 250,
                "total_slots": 12,
                "date_available": today,
                "date_deadline": today + timedelta(days=30),
                "duration_minutes": 45,
            },
            {
                "name": "Emergency Dental Care",
                "category": "emergency",
                "description": "Walk-in emergency dental assessment and treatment for acute pain, swelling, or trauma.",
                "estimated_cost": 35,
                "market_cost": 400,
                "total_slots": 5,
                "date_available": today,
                "date_deadline": today + timedelta(days=90),
                "duration_minutes": 60,
            },
        ]

        for p in procedures:
            proc = Procedure(college_id=profile.id, **p)
            db.session.add(proc)

    # Add sample patients
    patients = [
        {
            "email": "maria.garcia@example.com",
            "password": "demo123",
            "first_name": "Maria",
            "last_name": "Garcia",
            "phone": "(212) 555-0101",
            "zip_code": "10001",
            "date_of_birth": date(1988, 5, 14),
            "medical_notes": "No known allergies.",
        },
        {
            "email": "james.wilson@example.com",
            "password": "demo123",
            "first_name": "James",
            "last_name": "Wilson",
            "phone": "(215) 555-0202",
            "zip_code": "19107",
            "date_of_birth": date(1975, 11, 3),
            "medical_notes": "Type 2 diabetes, controlled with medication.",
        },
        {
            "email": "aisha.johnson@example.com",
            "password": "demo123",
            "first_name": "Aisha",
            "last_name": "Johnson",
            "phone": "(415) 555-0303",
            "zip_code": "94143",
            "date_of_birth": date(1995, 8, 22),
            "medical_notes": "",
        },
    ]

    for p in patients:
        user = User(email=p["email"], role="patient")
        user.set_password(p["password"])
        db.session.add(user)
        db.session.flush()

        coords = get_coordinates(p["zip_code"])
        profile = PatientProfile(
            user_id=user.id,
            first_name=p["first_name"],
            last_name=p["last_name"],
            phone=p["phone"],
            date_of_birth=p["date_of_birth"],
            zip_code=p["zip_code"],
            latitude=coords[0] if coords else None,
            longitude=coords[1] if coords else None,
            has_insurance=False,
            medical_notes=p["medical_notes"],
        )
        db.session.add(profile)

    db.session.commit()
    print(f"Seeded {len(colleges)} colleges with procedures and {len(patients)} sample patients.")
