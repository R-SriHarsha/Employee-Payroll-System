from flask import Blueprint, request, session, jsonify
from app.database import SessionLocal
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("employee_auth", __name__, url_prefix="/employee_auth")

@bp.route("/login", methods=["POST"])
def login():
    session.clear() 
    data = request.json
    db = SessionLocal()
    
    user = db.query(User).filter(
        User.username == data.get("username")
    ).first()
    
    if not user or user.role != "employee" or not check_password_hash(user.password, data.get("password")):
        db.close()
        return {"error": "Invalid username or password"}, 401

    session["employee_id"] = user.id
    session["user"] = user.username
    db.close()

    return jsonify({
        "message": "Login successful",
        "token": "simulated-employee-token-12345",
        "username": user.username,
        "employee_id": user.id
    })

@bp.route("/me", methods=["GET"])
def get_current_user():
    if "employee_id" not in session:
        return {"error": "Unauthorized"}, 401

    return {
        "employee_id": session["employee_id"],
        "username": session.get("user")
    }


@bp.route("/check", methods=["GET"])
def check():
    if "employee_id" in session:
        return jsonify({"employee_id": session["employee_id"]})
    return jsonify({"error": "Unauthorized"}), 401


@bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"})
