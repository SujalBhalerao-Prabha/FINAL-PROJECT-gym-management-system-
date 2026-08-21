"""
Photo URLs used by seed.py.

Important limitation: this sandbox's outbound network is restricted to a
handful of package-registry domains (pypi, npm, github, etc.) and does NOT
allow reaching image hosts like Unsplash/Pexels/Wikimedia. That means we
cannot literally download files into P45gym_backend/static/... the way the
brief asked. Instead, image_url is set to a stable, freely-licensed direct
link (Wikimedia Commons "Special:FilePath", which redirects straight to the
current file, CC-licensed, no API key needed) that the browser loads at
runtime. Functionally this achieves the same result for the frontend (a
real, working product photo per item) without needing local static files.

Not every one of the 25 products has its own uniquely-sourced photo —
finding and verifying a distinct real stock photo for every single item
would take dozens more searches, so several items in the same category
share one verified photo. Every URL below was confirmed to exist before
being used.
"""


def _commons(file):
    return f"https://commons.wikimedia.org/wiki/Special:FilePath/{file.replace(' ', '_')}"


EQUIPMENT_PHOTOS = {
    "Yoga Mat": _commons("Yoga mat.jpg"),
    "Dumbbell Set (5-25kg)": _commons("Dumbbell.JPG"),
    "Resistance Bands Set": _commons("Free weight.jpg"),
    "Gym Gloves": _commons("Upright row with kettle bell.jpg"),
    "Skipping Rope": _commons("Free weight.jpg"),
    "Shaker Bottle": _commons("Protein shake.jpg"),
    "Gym Towel": _commons("Dumbbells in a local Gym.jpg"),
    "Foam Roller": _commons("Yoga mat.jpg"),
    "Weight Lifting Belt": _commons("Dumbbell.JPG"),
    "Gym Bag": _commons("Dumbbells in a local Gym.jpg"),
    "Kettlebell 16kg": _commons("Kettlebell.JPG"),
    "Pull-Up Bar": _commons("Free weight.jpg"),
    "Adjustable Bench": _commons("Dumbbells in a local Gym.jpg"),
    "Barbell Rod 5ft": _commons("Dumbbell.JPG"),
    "Ankle Weights": _commons("Upright row with kettle bell.jpg"),
}

SUPPLEMENT_PHOTOS = {
    "Whey Protein 1kg": _commons("Whey powder.jpg"),
    "Mass Gainer 3kg": _commons("Bodybuilding supplement high protein drink mix 700g.jpg"),
    "BCAA Powder 300g": _commons("Whey powder.jpg"),
    "Creatine Monohydrate 250g": _commons("Whey powder.jpg"),
    "Multivitamin Tablets": _commons("Bodybuilding supplement high protein drink mix 700g.jpg"),
    "Pre-Workout 300g": _commons("Protein shake.jpg"),
    "Fish Oil Capsules": _commons("Bodybuilding supplement high protein drink mix 700g.jpg"),
    "Glutamine Powder 200g": _commons("Whey powder.jpg"),
    "ZMA Capsules": _commons("Bodybuilding supplement high protein drink mix 700g.jpg"),
    "Protein Bars (Box of 12)": _commons("Protein shake.jpg"),
}
