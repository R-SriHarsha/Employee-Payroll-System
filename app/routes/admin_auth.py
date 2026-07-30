from flask import Blueprint, request, jsonify, session
from app.database import SessionLocal
from app.models.user import User

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login", methods=["POST"])
def login_admin():
    session.clear()
    data = request.json

    db = SessionLocal()

    user = db.query(User).filter(
        User.username == data.get("username"),
        User.password == data.get("password")
    ).first()

    db.close()

    if not user or user.role != "admin":
        return jsonify({
            "error": "Invalid credentials or not an admin"
        }), 401

    session["admin_id"] = user.id
    session["username"] = user.username

    return jsonify({
        "message": "Login successful",
        "token": "simulated-admin-token-12345",
        "username": user.username,
        "role": user.role
    })


@bp.route("/check", methods=["GET"])
def check_admin():
    if "admin_id" in session:
        return jsonify({"authenticated": True, "username": session.get("username")})
    return jsonify({"authenticated": False}), 401

@bp.route("/logout", methods=["POST"])
def logout_admin():
    session.clear()
    return jsonify({"message": "Logged out"})
