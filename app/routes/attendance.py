from flask import Blueprint, request, jsonify
from app.database import SessionLocal
from app.models.attendance import Attendance

bp = Blueprint("attendance", __name__, url_prefix="/attendance")



@bp.route("/monthly", methods=["POST"])
def add_monthly_attendance():
    data = request.json
    db = SessionLocal()

    employee_id = data.get("employee_id")
    month = data.get("month")
    year = data.get("year")
    present_days = data.get("present_days", 0)
    leaves = data.get("leaves", 0)

    if not all([employee_id, month, year]):
        db.close()
        return jsonify({"error": "Missing required fields"}), 400

    record = db.query(Attendance).filter(
        Attendance.employee_id == employee_id,
        Attendance.month == month,
        Attendance.year == year
    ).first()

    if record:
        record.present_days = present_days
        record.leaves = leaves
    else:
        record = Attendance(
            employee_id=employee_id,
            month=month,
            year=year,
            present_days=present_days,
            leaves=leaves
        )
        db.add(record)

    db.commit()
    db.close()

    return jsonify({"message": "Monthly attendance recorded successfully"})


@bp.route("/", methods=["GET"])
def get_attendance():
    db = SessionLocal()
    records = db.query(Attendance).all()

    result = []
    for r in records:
        result.append({
            "employee_id": r.employee_id,
            "month": r.month,
            "year": r.year,
            "present_days": r.present_days,
            "absent_days": r.absent_days
        })

    db.close()
    return jsonify(result)
