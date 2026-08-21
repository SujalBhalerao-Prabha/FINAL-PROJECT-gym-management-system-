from flask import Flask
from flask_cors import CORS

from config import Config
from database.db import db
from routes.member_routes import member_bp
from routes.plan_routes import plan_bp
from routes.membership_routes import membership_bp
from routes.equipment_routes import equipment_bp
from routes.supplement_routes import supplement_bp

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)

db.init_app(app)

app.register_blueprint(member_bp)
app.register_blueprint(plan_bp)
app.register_blueprint(membership_bp)
app.register_blueprint(equipment_bp)
app.register_blueprint(supplement_bp)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return {
        "msg": "Gym Management System"
    }


if __name__ == "__main__":
    app.run(debug=True)
