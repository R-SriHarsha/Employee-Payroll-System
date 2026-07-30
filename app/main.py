import os
from flask import Flask, send_from_directory
from app.routes.auth import bp as auth_bp
from app.database import Base, engine
from app.routes import employee, attendance, payroll, admin_auth, leave
from app.routes.report import bp as report_bp
from app.models.leave import LeaveRequest

# Create tables
Base.metadata.create_all(bind=engine)

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Flask app
app = Flask(__name__)
app.secret_key = "super-secret-key"

# ------------------ FRONTEND ROUTES ------------------

@app.route("/")
def index():
    return send_from_directory(os.path.join(BASE_DIR, "frontend"), "index.html")

@app.route("/admin.html")
def admin_page():
    return send_from_directory(os.path.join(BASE_DIR, "frontend"), "admin.html")

@app.route("/employee.html")
def employee_page():
    return send_from_directory(os.path.join(BASE_DIR, "frontend"), "employee.html")

@app.route("/style.css")
def style():
    return send_from_directory(os.path.join(BASE_DIR, "frontend"), "style.css")

@app.route("/script.js")
def script():
    return send_from_directory(os.path.join(BASE_DIR, "frontend"), "script.js")

@app.route("/payslip.html")
def payslip_page():
    return send_from_directory(os.path.join(BASE_DIR, "frontend"), "payslip.html")

# ------------------ REGISTER ROUTES ------------------

app.register_blueprint(employee.bp)
app.register_blueprint(attendance.bp)
app.register_blueprint(payroll.bp)
app.register_blueprint(admin_auth.bp)
app.register_blueprint(report_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(leave.bp)


# ------------------ RUN SERVER ------------------

if __name__ == "__main__":
    app.run(debug=True)
