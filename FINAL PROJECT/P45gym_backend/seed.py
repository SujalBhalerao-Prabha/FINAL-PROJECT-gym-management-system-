"""
Clears and repopulates the database with demo data:
  - 20 members (Indian cricketers)
  - 10 plans
  - 10 memberships (linking members 1-10 to plans 1-10)
  - 15 equipment items, each with a verified real product photo
  - 10 supplements, each with a verified real product photo

See seed_photos.py for a note on why image_url points to Wikimedia Commons
links rather than local static files.

Usage:
    python seed.py
"""

from app import app
from database.db import db
from models.member_model import Member
from models.plan_model import Plan
from models.membership_model import Membership
from models.equipment_model import Equipment
from models.supplement_model import Supplement
from seed_photos import EQUIPMENT_PHOTOS, SUPPLEMENT_PHOTOS

# ---- Members (name, age) — email/phone are generated below ----
MEMBERS = [
    ("Virat Kohli", 38),
    ("Rohit Sharma", 39),
    ("MS Dhoni", 45),
    ("Jasprit Bumrah", 33),
    ("Hardik Pandya", 33),
    ("KL Rahul", 34),
    ("Ravindra Jadeja", 38),
    ("Shubman Gill", 27),
    ("Rishabh Pant", 29),
    ("Suryakumar Yadav", 36),
    ("Sachin Tendulkar", 53),
    ("Rahul Dravid", 53),
    ("Yuvraj Singh", 45),
    ("Shikhar Dhawan", 41),
    ("Bhuvneshwar Kumar", 36),
    ("Mohammed Shami", 36),
    ("Axar Patel", 32),
    ("Yashasvi Jaiswal", 25),
    ("Ishan Kishan", 28),
    ("Kuldeep Yadav", 32),
]

# ---- Plans (name, duration_months, price, status) ----
PLANS = [
    ("1 Month Basic", 1, 1500, "Active"),
    ("3 Month Standard", 3, 4000, "Active"),
    ("6 Month Standard", 6, 7500, "Active"),
    ("12 Month Premium", 12, 14000, "Active"),
    ("1 Month Cardio Only", 1, 1200, "Active"),
    ("3 Month Strength", 3, 4500, "Active"),
    ("6 Month Premium", 6, 9000, "Active"),
    ("Student Monthly", 1, 999, "Active"),
    ("Couple Plan 3 Month", 3, 7000, "Active"),
    ("Senior Citizen Plan", 6, 6000, "Inactive"),
]

# ---- Memberships (member_index, plan_index, start_date, end_date) — 0-based ----
MEMBERSHIPS = [
    (0, 0, "2026-01-05", "2026-02-05"),
    (1, 1, "2026-01-10", "2026-04-10"),
    (2, 2, "2026-02-01", "2026-08-01"),
    (3, 3, "2026-01-01", "2027-01-01"),
    (4, 4, "2026-03-01", "2026-04-01"),
    (5, 5, "2026-02-15", "2026-05-15"),
    (6, 6, "2026-01-20", "2026-07-20"),
    (7, 7, "2026-04-01", "2026-05-01"),
    (8, 8, "2026-03-10", "2026-06-10"),
    (9, 9, "2026-01-15", "2026-07-15"),
]

# ---- Equipment (name, category, price, stock_quantity, status) ----
EQUIPMENT = [
    ("Yoga Mat", "Workout Accessories", 899, 40, "In Stock"),
    ("Dumbbell Set (5-25kg)", "Workout Accessories", 12999, 8, "In Stock"),
    ("Resistance Bands Set", "Workout Accessories", 699, 25, "In Stock"),
    ("Gym Gloves", "Gym Essentials", 449, 30, "In Stock"),
    ("Skipping Rope", "Workout Accessories", 299, 35, "In Stock"),
    ("Shaker Bottle", "Useful Extras", 249, 50, "In Stock"),
    ("Gym Towel", "Gym Essentials", 199, 45, "In Stock"),
    ("Foam Roller", "Workout Accessories", 999, 15, "In Stock"),
    ("Weight Lifting Belt", "Workout Accessories", 1299, 12, "In Stock"),
    ("Gym Bag", "Gym Essentials", 1499, 20, "In Stock"),
    ("Kettlebell 16kg", "Workout Accessories", 2999, 10, "In Stock"),
    ("Pull-Up Bar", "Workout Accessories", 1799, 0, "Out of Stock"),
    ("Adjustable Bench", "Workout Accessories", 6999, 6, "In Stock"),
    ("Barbell Rod 5ft", "Workout Accessories", 3499, 9, "In Stock"),
    ("Ankle Weights", "Workout Accessories", 899, 18, "In Stock"),
]

# ---- Supplements (name, category, price, stock_quantity, expiry_date, status) ----
SUPPLEMENTS = [
    ("Whey Protein 1kg", "Protein", 2499, 30, "2027-06-30", "In Stock"),
    ("Mass Gainer 3kg", "Weight Gain", 3299, 20, "2027-08-31", "In Stock"),
    ("BCAA Powder 300g", "Other", 1199, 25, "2027-05-31", "In Stock"),
    ("Creatine Monohydrate 250g", "Other", 899, 40, "2027-12-31", "In Stock"),
    ("Multivitamin Tablets", "Vitamins", 599, 50, "2028-01-31", "In Stock"),
    ("Pre-Workout 300g", "Pre-Workout", 1799, 15, "2027-04-30", "In Stock"),
    ("Fish Oil Capsules", "Vitamins", 799, 35, "2027-09-30", "In Stock"),
    ("Glutamine Powder 200g", "Other", 999, 0, "2027-07-31", "Out of Stock"),
    ("ZMA Capsules", "Vitamins", 899, 22, "2027-10-31", "In Stock"),
    ("Protein Bars (Box of 12)", "Protein", 1099, 28, "2026-12-31", "In Stock"),
]


def slugify_email(name):
    parts = name.lower().split()
    return f"{parts[0]}.{parts[-1]}@example.com"


with app.app_context():
    print("Clearing existing data...")
    Membership.query.delete()
    Equipment.query.delete()
    Supplement.query.delete()
    Plan.query.delete()
    Member.query.delete()
    db.session.commit()

    print("Seeding members...")
    member_rows = []
    phone_start = 9876543210
    for i, (name, age) in enumerate(MEMBERS):
        member = Member(
            name=name,
            email=slugify_email(name),
            phone=str(phone_start + i),
            age=age
        )
        db.session.add(member)
        member_rows.append(member)
    db.session.flush()  # assign ids without committing yet

    print("Seeding plans...")
    plan_rows = []
    for plan_name, duration, price, status in PLANS:
        plan = Plan(plan_name=plan_name, duration_months=duration, price=price, status=status)
        db.session.add(plan)
        plan_rows.append(plan)
    db.session.flush()

    print("Seeding memberships...")
    for member_idx, plan_idx, start, end in MEMBERSHIPS:
        db.session.add(Membership(
            member_id=member_rows[member_idx].id,
            plan_id=plan_rows[plan_idx].id,
            start_date=start,
            end_date=end,
            status="Active"
        ))

    print("Seeding equipment...")
    for name, category, price, qty, status in EQUIPMENT:
        db.session.add(Equipment(
            product_name=name,
            category=category,
            price=price,
            stock_quantity=qty,
            status=status,
            image_url=EQUIPMENT_PHOTOS.get(name)
        ))

    print("Seeding supplements...")
    for name, category, price, qty, expiry, status in SUPPLEMENTS:
        db.session.add(Supplement(
            product_name=name,
            category=category,
            price=price,
            stock_quantity=qty,
            expiry_date=expiry,
            status=status,
            image_url=SUPPLEMENT_PHOTOS.get(name)
        ))

    db.session.commit()
    print(
        f"Done. Seeded {len(MEMBERS)} members, {len(PLANS)} plans, "
        f"{len(MEMBERSHIPS)} memberships, {len(EQUIPMENT)} equipment items, "
        f"{len(SUPPLEMENTS)} supplements."
    )
