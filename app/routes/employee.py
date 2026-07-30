from flask import Blueprint, request, jsonify
from app.database import SessionLocal
from app.models.employee import Employee

from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("employee", __name__, url_prefix="/employees")

# ------------------------
# Create Employee
# ------------------------
@bp.route("/", methods=["POST"])
def create_employee():
    data = request.json
    db = SessionLocal()

    password = data.pop("password", "password123")

    employee = Employee(**data)
    db.add(employee)
    db.commit()
    db.refresh(employee)

    username = f"{employee.id}"

    user = User(
        id=employee.id,  # SAME ID
        username=username,
        password=generate_password_hash(password),
        role="employee"
    )

    db.add(user)
    db.commit()

    result = {
        "id": employee.id,
        "name": employee.name,
        "department": employee.department,
        "designation": employee.designation,
        "base_salary": employee.base_salary,
        "username": username,
        "default_password": default_password  
    }
    

    db.close()
    return jsonify(result)


# ------------------------
# Get All Employees
# ------------------------
@bp.route("/", methods=["GET"])
def get_employees():
    db = SessionLocal()

    employees = db.query(Employee).all()

    result = []
    for emp in employees:
        result.append({
            "id": emp.id,
            "name": emp.name,
            "department": emp.department,
            "designation": emp.designation,
            "base_salary": emp.base_salary
        })

    db.close()
    return jsonify(result)


# ------------------------
# Get Single Employee
# ------------------------
@bp.route("/<int:employee_id>", methods=["GET"])
def get_employee(employee_id):
    db = SessionLocal()

    emp = db.query(Employee).filter(Employee.id == employee_id).first()

    if not emp:
        db.close()
        return jsonify({"error": "Employee not found"}), 404

    result = {
        "id": emp.id,
        "name": emp.name,
        "department": emp.department,
        "designation": emp.designation,
        "base_salary": emp.base_salary
    }

    db.close()
    return jsonify(result)


# ------------------------
# Update Employee
# ------------------------
@bp.route("/<int:employee_id>", methods=["PUT"])
def update_employee(employee_id):
    data = request.json
    db = SessionLocal()

    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if not employee:
        db.close()
        return jsonify({"error": "Employee not found"}), 404

    employee.name = data.get("name")
    employee.department = data.get("department")
    employee.designation = data.get("designation")
    employee.base_salary = data.get("base_salary")

    db.commit()
    db.refresh(employee)

    result = {
        "id": employee.id,
        "name": employee.name,
        "department": employee.department,
        "designation": employee.designation,
        "base_salary": employee.base_salary
    }

    db.close()
    return jsonify(result)


# ------------------------
# Delete Employee
# ------------------------
@bp.route("/<int:employee_id>", methods=["DELETE"])
def delete_employee(employee_id):
    db = SessionLocal()

    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if not employee:
        db.close()
        return jsonify({"error": "Employee not found"}), 404

    # Delete corresponding user
    user = db.query(User).filter(User.id == employee_id).first()
    if user:
        db.delete(user)

    db.delete(employee)
    db.commit()
    db.close()

    return jsonify({"message": "Employee deleted successfully"})
