from flask import Blueprint, request, jsonify
from app.database import SessionLocal
from app.models.leave import LeaveRequest
from datetime import datetime

bp = Blueprint("leave", __name__, url_prefix="/leaves")

# Apply for leave (Employee)
@bp.route("/", methods=["POST"])
def apply_leave():
    data = request.json
    db = SessionLocal()

    try:
        start_date = datetime.strptime(data.get("start_date"), "%Y-%m-%d").date()
        end_date = datetime.strptime(data.get("end_date"), "%Y-%m-%d").date()
        
        leave_request = LeaveRequest(
            employee_id=data.get("employee_id"),
            start_date=start_date,
            end_date=end_date,
            reason=data.get("reason"),
            status="Pending"
        )
        
        db.add(leave_request)
        db.commit()
        db.close()
        return jsonify({"message": "Leave request submitted successfully"})
    except Exception as e:
        db.close()
        return jsonify({"error": str(e)}), 400

# Get leaves for a specific employee
@bp.route("/employee/<int:employee_id>", methods=["GET"])
def get_employee_leaves(employee_id):
    db = SessionLocal()
    leaves = db.query(LeaveRequest).filter(LeaveRequest.employee_id == employee_id).all()
    
    result = []
    for l in leaves:
        result.append({
            "id": l.id,
            "start_date": l.start_date.strftime("%Y-%m-%d"),
            "end_date": l.end_date.strftime("%Y-%m-%d"),
            "reason": l.reason,
            "status": l.status
        })

    db.close()
    return jsonify(result)

# Get all leaves (Admin)
@bp.route("/", methods=["GET"])
def get_all_leaves():
    db = SessionLocal()
    leaves = db.query(LeaveRequest).all()
    
    result = []
    for l in leaves:
        result.append({
            "id": l.id,
            "employee_id": l.employee_id,
            "start_date": l.start_date.strftime("%Y-%m-%d"),
            "end_date": l.end_date.strftime("%Y-%m-%d"),
            "reason": l.reason,
            "status": l.status
        })

    db.close()
    return jsonify(result)

# Update leave status (Admin)
@bp.route("/<int:leave_id>", methods=["PUT"])
def update_leave_status(leave_id):
    data = request.json
    db = SessionLocal()
    
    leave_request = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()
    if not leave_request:
        db.close()
        return jsonify({"error": "Leave request not found"}), 404
        
    new_status = data.get("status")
    if new_status in ["Approved", "Rejected"]:
        leave_request.status = new_status
        db.commit()
        
    db.close()
    return jsonify({"message": f"Leave status updated to {new_status}"})
