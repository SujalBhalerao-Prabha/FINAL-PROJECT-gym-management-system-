"""
Run this once after starting the app for the first time to preload
the equipment and supplement catalog with the products you listed.

Usage:
    python seed_data.py
"""

from app import app
from database.db import db
from models.equipment_model import Equipment
from models.supplement_model import Supplement

equipment_catalog = {
    "Gym Essentials": [
        "Gym Bag", "Gym Shoes / Training Shoes", "Water Bottle", "Gym Towel",
        "Workout Gloves", "Socks", "Sports / Activewear T-Shirts",
        "Shorts / Track Pants", "Sports Bra (Women)", "Headband / Cap", "Sweat Towel"
    ],
    "Workout Accessories": [
        "Hand Gripper", "Wrist Wraps", "Lifting Straps", "Knee Sleeves",
        "Elbow Sleeves", "Resistance Bands", "Skipping Rope", "Yoga / Exercise Mat",
        "Foam Roller", "Massage Ball", "Ab Roller", "Ankle Straps", "Weightlifting Belt"
    ],
    "Personal Care": [
        "Deodorant", "Face / Body Towel", "Shower Gel", "Shampoo", "Comb",
        "Hand Sanitizer", "Small Toiletry Bag"
    ],
    "Useful Extras": [
        "Gym Locker Lock", "Earphones / Headphones", "Phone Armband",
        "Fitness Tracker / Smartwatch", "Protein Shaker", "Meal Container",
        "Small First-Aid Kit"
    ]
}

supplement_catalog = {
    "Supplements": [
        "Whey Protein", "Creatine Monohydrate", "Mass Gainer", "Whey Isolate",
        "Casein Protein", "Electrolytes", "Caffeine / Pre-Workout", "Protein Bars",
        "BCAA / EAA", "Omega-3", "Multivitamin", "Glutamine"
    ]
}

with app.app_context():
    db.create_all()

    for category, products in equipment_catalog.items():
        for name in products:
            exists = Equipment.query.filter_by(product_name=name).first()
            if not exists:
                db.session.add(Equipment(
                    product_name=name,
                    category=category,
                    price=0,
                    stock_quantity=0,
                    status="In Stock"
                ))

    for category, products in supplement_catalog.items():
        for name in products:
            exists = Supplement.query.filter_by(product_name=name).first()
            if not exists:
                db.session.add(Supplement(
                    product_name=name,
                    category=category,
                    price=0,
                    stock_quantity=0,
                    expiry_date=None,
                    status="In Stock"
                ))

    db.session.commit()
    print("Equipment and Supplement catalog seeded successfully.")
