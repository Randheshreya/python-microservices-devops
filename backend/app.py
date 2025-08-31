# backend/app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate   # ✅ Added
import os, requests

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/postgres"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB + Migrations
db = SQLAlchemy(app)
migrate = Migrate(app, db)   # ✅ Added

# Models
class User(db.Model):
    __tablename__ = "users"   # ✅ explicit table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

# Routes
@app.route("/api/data", methods=["GET", "POST"])
def data():
    if request.method == "POST":
        payload = request.json or {}
        name = payload.get("name", "anonymous")
        u = User(name=name)
        db.session.add(u)
        db.session.commit()

        # Send log to logger service
        logger_url = os.getenv("LOGGER_URL", "http://logger:6000/log")
        try:
            requests.post(logger_url, json={"event": "new_user", "name": name}, timeout=2)
        except Exception:
            pass

        return jsonify({"id": u.id, "name": u.name}), 201

    # GET request -> return all users
    users = User.query.all()
    return jsonify([{"id": u.id, "name": u.name} for u in users])
