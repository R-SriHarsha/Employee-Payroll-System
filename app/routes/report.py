from flask import Blueprint, jsonify, request
from app.database import SessionLocal
from app.models.payroll import Payroll
from app.models.employee import Employee
from app.models.attendance import Attendance

bp = Blueprint("reports", __name__, url_prefix="/reports")


# --------------------------
# Monthly Payroll Report
# --------------------------
@bp.route("/payroll", methods=["GET"])
def monthly_payroll_report():
    db = SessionLocal()

    month = request.args.get("month")
    year = request.args.get("year")

    payrolls = db.query(Payroll).filter(
        Payroll.month == month,
        Payroll.year == year
    ).all()

    result = []
    total_salary = 0

    for p in payrolls:
        emp = db.query(Employee).filter(Employee.id == p.employee_id).first()

        result.append({
            "employee_id": p.employee_id,
            "name": emp.name,
            "net_salary": p.net_salary
        })

        total_salary += p.net_salary

    db.close()

    return jsonify({
        "data": result,
        "total_salary": total_salary
    })


# --------------------------
# Attendance Report
# --------------------------
@bp.route("/attendance", methods=["GET"])
def attendance_report():
    db = SessionLocal()

    month = request.args.get("month")
    year = request.args.get("year")

    records = db.query(Attendance).filter(
        Attendance.month == month,
        Attendance.year == year
    ).all()

    result = []

    for r in records:
        emp = db.query(Employee).filter(Employee.id == r.employee_id).first()

        result.append({
            "employee_id": r.employee_id,
            "name": emp.name,
            "present_days": r.present_days,
            "leaves": r.leaves
        })

    db.close()

    return jsonify(result)
