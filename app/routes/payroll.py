from flask import Blueprint, request, jsonify, send_file
from app.database import SessionLocal
from app.models.employee import Employee
from app.models.payroll import Payroll
from sqlalchemy import extract
from app.services.payroll_service import calculate_salary
from app.models.attendance import Attendance

import os

bp = Blueprint("payroll", __name__, url_prefix="/payroll")

# ------------------------
# Run Payroll
# ------------------------
@bp.route("/run", methods=["POST"])
def run_payroll():
    data = request.json
    db = SessionLocal()

    employee_id = data.get("employee_id")
    month = data.get("month")
    year = data.get("year")

    # 👉 Step 1: Get employee
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        return {"error": "Employee not found"}


    # 👉 Step 2: Get base salary
    base_salary = employee.base_salary

    # 👉 Step 3: Fetch Monthly attendance
    attendance_record = db.query(Attendance).filter(
        Attendance.employee_id == employee_id,
        Attendance.month == month,
        Attendance.year == year
    ).first()

    if not attendance_record:
        db.close()
        return {"error": f"Attendance record not found for {month}/{year}. Please update attendance first."}, 400
    
    present_days = attendance_record.present_days

    # 👉 Step 5: Calculate salary
    salary_data = calculate_salary(base_salary, present_days)

    # 👉 Step 6: Save payroll
    # 👉 Step 6: Check if payroll already exists
    existing_payroll = db.query(Payroll).filter(
        Payroll.employee_id == employee_id,
        Payroll.month == month,
        Payroll.year == year
    ).first()

    if existing_payroll:
        # UPDATE existing record
        existing_payroll.basic_salary = salary_data["basic"]
        existing_payroll.hra = salary_data["hra"]
        existing_payroll.da = salary_data["da"]
        existing_payroll.pf = salary_data["pf"]
        existing_payroll.tax = salary_data["tax"]
        existing_payroll.gross_salary = salary_data["gross"]
        existing_payroll.net_salary = salary_data["net"]
    else:
        # INSERT new record
        payroll = Payroll(
        employee_id=employee_id,
        month=month,
        year=year,
        basic_salary=salary_data["basic"],
        hra=salary_data["hra"],
        da=salary_data["da"],
        pf=salary_data["pf"],
        tax=salary_data["tax"],
        gross_salary=salary_data["gross"],
        net_salary=salary_data["net"]
    )
        db.add(payroll)
    


    # 🔥 STEP 7: COMMIT EVERYTHING
    db.commit()
    db.close()

    return {"message": "Payroll processed successfully"}




@bp.route("/", methods=["GET"])
def get_all_payrolls():
    db = SessionLocal()

    payrolls = db.query(Payroll).all()

    result = []
    for p in payrolls:
        result.append({
            "id": p.id,
            "employee_id": p.employee_id,
            "month": p.month,
            "year": p.year,
            "net_salary": p.net_salary
        })

    db.close()
    return jsonify(result)


# ------------------------
# Get Employee Payrolls
# ------------------------
@bp.route("/<int:employee_id>", methods=["GET"])
def get_employee_payrolls(employee_id):
    db = SessionLocal()

    payrolls = db.query(Payroll).filter(
        Payroll.employee_id == employee_id
    ).all()

    result = []
    for p in payrolls:
        result.append({
            "id": p.id,
            "month": p.month,
            "year": p.year,
            "net_salary": p.net_salary,
            "basic_salary": p.basic_salary,
            "hra": p.hra,
            "da": p.da,
            "pf": p.pf,
            "tax": p.tax,
            "gross_salary": p.gross_salary,
        })

    db.close()
    return jsonify(result)


# ------------------------
# Download Payslip
# ------------------------
@bp.route("/<int:employee_id>/download/<int:month>/<int:year>", methods=["GET"])
def download_payslip(employee_id, month, year):
    db = SessionLocal()

    emp = db.query(Employee).filter(Employee.id == employee_id).first()

    payroll = db.query(Payroll).filter(
        Payroll.employee_id == employee_id,
        Payroll.month == month,
        Payroll.year == year
    ).first()

    if not emp or not payroll:
        db.close()
        return jsonify({"error": "Payslip data not found"}), 404

    attendance = db.query(Attendance).filter(
        Attendance.employee_id == employee_id,
        Attendance.month == month,
        Attendance.year == year
    ).first()
    
    payslip_data = {
        "employee": {
            "id": emp.id,
            "name": emp.name,
            "department": emp.department,
            "designation": emp.designation
        },
        "attendance": {
            "total_days": 30,
            "present_days": attendance.present_days if attendance else 30
        },
        "salary": {
            "basic": payroll.basic_salary,
            "hra": payroll.hra,
            "da": payroll.da,
            "pf": payroll.pf,
            "tax": payroll.tax,
            "gross": payroll.gross_salary,
            "net": payroll.net_salary
        }
    }

    db.close()
    return jsonify(payslip_data)
