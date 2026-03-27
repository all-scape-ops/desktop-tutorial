# DentalConnect

An open-source web app that connects people **without dental insurance** to **dental colleges** offering affordable, supervised care.

Students get real-world clinical experience. Patients get quality dental care at a fraction of the cost.

## How It Works

1. **Search** - Enter your zip code to find dental colleges near you with open procedure slots
2. **Apply** - Submit an application describing your dental needs and urgency level
3. **Get Treated** - Once accepted, receive a confirmation code and show up for your appointment

### Priority System

Applications are ranked by health urgency, then first-come-first-served:

| Tier | Level | Description |
|------|-------|-------------|
| 1 | **Emergency** | Severe pain, trauma, infection - reviewed first |
| 2 | **Pain** | Ongoing discomfort affecting daily life |
| 3 | **Routine** | Preventive care, checkups, cleanings |

Within each tier, earlier applications get higher priority. If all slots fill, you're automatically waitlisted and promoted when a spot opens.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Seed the database with sample data (6 dental colleges, 36 procedures, 3 patients)
flask seed

# Run the app
python run.py
```

Then open http://localhost:5000 in your browser.

### Demo Accounts

| Role | Email | Password |
|------|-------|----------|
| Patient | maria.garcia@example.com | demo123 |
| Patient | james.wilson@example.com | demo123 |
| College | admin@nyudental.example.com | demo123 |
| College | admin@upenn-dental.example.com | demo123 |

## Features

**For Patients:**
- Search dental colleges by zip code and distance
- Browse available procedures with cost savings displayed
- Apply with urgency-based priority ranking
- Track application status and upcoming appointments
- Receive confirmation codes for reservations

**For Dental Colleges:**
- Post procedures with costs, slots, and deadlines
- View applications ranked by priority score
- Accept/reject applications with appointment scheduling
- Manage reservations and mark completions
- Automatic waitlist management

## Tech Stack

- **Backend:** Python / Flask
- **Database:** SQLite (via SQLAlchemy)
- **Frontend:** HTML / Bootstrap 5 / Jinja2
- **Auth:** Flask-Login with password hashing
- **Forms:** Flask-WTF with validation
- **Location:** Bundled US zip code dataset with Haversine distance

No external APIs, databases, or build tools required. Clone, install, run.

## Project Structure

```
app/
  __init__.py          # App factory
  models.py            # Database models (6 tables)
  matching.py          # Priority scoring engine
  forms.py             # WTForms validation
  geo.py               # Zip code lookup + distance calc
  seed.py              # Sample data loader
  blueprints/
    auth.py            # Login, registration, logout
    main.py            # Landing page, search, college detail
    patient.py         # Patient dashboard, apply, applications
    college.py         # College dashboard, procedures, accept/reject
  templates/           # Jinja2 HTML templates
  static/              # CSS + JS
  data/
    zipcodes.csv       # US zip code coordinates
```
