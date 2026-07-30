# Employee Payroll System

A comprehensive and robust full-stack web application for managing employee profiles, attendance, payroll processing, leave management, and monthly reports. The system is designed with a role-based access control paradigm separating Administrator and Employee roles.

---

## 🚀 Features

### 🔑 Authentication & Roles
- **Admins**: Login using credentials seeded in the system. Full access to administrative dashboard capabilities.
- **Employees**: Login using their Employee ID as their username and a custom password generated upon registration.

### 👥 Employee Management
- Complete CRUD (Create, Read, Update, Delete) capability on employee records.
- Automatically creates matching user credentials when an employee is registered.

  <img width="946" height="473" alt="Screenshot 2026-07-30 131100" src="https://github.com/user-attachments/assets/cf8a7ea0-7274-4dfa-b62d-cc9d0f9d1861" />


### 📅 Attendance & Leave Management
- **Attendance**: Record monthly active/present days and leaves.
- **Leaves**: Employees can apply for leaves by specifying start/end dates and reasons. Admins can view all leave requests and approve/reject them in real-time.
  <img width="959" height="444" alt="Screenshot 2026-07-30 131113" src="https://github.com/user-attachments/assets/403a5388-db8d-4352-baf9-3e2e98557f2c" />


### 💰 Payroll Processing
- Computes salary details dynamically based on base salary and present days (out of a 30-day standard month):
  - **Basic Salary**: Pro-rated base salary based on present days.
  - **HRA (House Rent Allowance)**: 30% of basic salary.
  - **DA (Dearness Allowance)**: 5% of basic salary.
  - **PF (Provident Fund)**: 12% of basic salary (capped at ₹1,800).
  - **Tax**: 5% of gross salary.
  - **Net Salary**: `Gross - (PF + Tax)`.
- Generates interactive, downloadable monthly payslips.

  <img width="419" height="440" alt="Screenshot 2026-07-30 131221" src="https://github.com/user-attachments/assets/5ad413fd-aa94-4b35-a47a-5d74b2ae660f" />


### 📊 Report Generation
- Generate monthly payroll reports showing individual net salaries and overall company expenditure.
- Generate monthly attendance reports summarizing present days and leaves per employee.

---

## 📂 Project Structure

```text
employee_payroll_system/
├── app/
│   ├── models/           # SQLAlchemy Database Models
│   │   ├── user.py       # User credentials and role definitions
│   │   ├── employee.py   # Employee personal and contract details
│   │   ├── attendance.py # Attendance tracking logs
│   │   ├── payroll.py    # Saved monthly salary computations
│   │   └── leave.py      # Leave application records
│   ├── routes/           # Flask Route Blueprints
│   │   ├── auth.py       # Employee auth endpoints
│   │   ├── admin_auth.py # Admin auth endpoints
│   │   ├── employee.py   # Employee registry routes
│   │   ├── attendance.py # Attendance submission routes
│   │   ├── payroll.py    # Payroll processing and payslips
│   │   ├── report.py     # Payroll and attendance reporting
│   │   └── leave.py      # Leave submission & approval routes
│   ├── services/         # Business Logic Layer
│   │   └── payroll_service.py # Core salary calculation engine
│   ├── database.py       # SQLAlchemy setup and engine initialization
│   └── main.py           # Application entry point and static content serving
├── frontend/             # Single-Page Frontend Client Files
│   ├── index.html        # Main Login Page
│   ├── admin.html        # Admin Operations Dashboard
│   ├── employee.html     # Employee Profile and Request Dashboard
│   ├── payslip.html      # Print-ready payslip viewer
│   ├── script.js         # Frontend interactive logic and API bindings
│   └── style.css         # Modern, responsive UI design styling
├── .env                  # Environment Variables (Database URL)
├── requirements.txt      # Python dependencies
└── seed_admin.py         # Admin database seeder
```

---

## 🛠️ Setup & Installation

### 1. Prerequisites
Ensure you have Python 3.8+ installed on your system.

### 2. Clone and Setup Environment
Navigate to the root directory and create a virtual environment:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
Install all required packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Configuration
Create a `.env` file in the root directory (or update the existing one) to specify your database connection.

By default, the application connects to a MySQL database:
```env
DATABASE_URL=mysql+pymysql://<username>:<password>@localhost:3306/<database_name>
```
*Note: If no database URL is provided, the application will automatically fall back to SQLite: `sqlite:///./fallback.db`.*

### 5. Database Initialization & Seeding Admin
Run the seeding script to automatically create database tables and seed the initial Administrator user:

```bash
python seed_admin.py
```
**Default Admin Credentials:**
- **Username**: `admin`
- **Password**: `password123`

---

## 🚀 Running the Application

Start the Flask development server:

```bash
python app/main.py
```

The application will launch locally at `http://127.0.0.1:5000/`.

- Visit `http://127.0.0.1:5000/` to access the Employee Login.
- Click the **Admin Panel** button in the top-right or go directly to `http://127.0.0.1:5000/admin.html` to access the Admin dashboard.

---

## 🔌 API Documentation Reference

The backend provides the following endpoints:

| Endpoint | Method | Role | Description |
| :--- | :---: | :---: | :--- |
| `/auth/login` | `POST` | Admin | Login as Administrator |
| `/auth/check` | `GET` | Admin | Check admin authentication status |
| `/auth/logout` | `POST` | Admin | Log out admin |
| `/employee_auth/login` | `POST` | Employee | Login as Employee |
| `/employee_auth/me` | `GET` | Employee | Retrieve current employee identity |
| `/employee_auth/logout` | `POST` | Employee | Log out employee |
| `/employees/` | `POST` | Admin | Create a new employee |
| `/employees/` | `GET` | Admin | Retrieve list of all employees |
| `/employees/<id>` | `GET` | All | Fetch details of a specific employee |
| `/employees/<id>` | `PUT` | Admin | Update employee record |
| `/employees/<id>` | `DELETE` | Admin | Delete employee record and user |
| `/attendance/monthly` | `POST` | Admin | Record/update monthly attendance records |
| `/leaves/` | `POST` | Employee | Submit a leave request |
| `/leaves/employee/<id>`| `GET` | Employee | Retrieve leave history for an employee |
| `/leaves/` | `GET` | Admin | View all leave requests |
| `/leaves/<id>` | `PUT` | Admin | Approve or reject a leave request |
| `/payroll/run` | `POST` | Admin | Calculate and save payroll details |
| `/payroll/` | `GET` | Admin | View all payroll records |
| `/payroll/<id>` | `GET` | Employee | View payroll history for an employee |
| `/payroll/<id>/download/<m>/<y>` | `GET` | All | Fetch details of a single payslip |
| `/reports/payroll` | `GET` | Admin | Generate monthly payroll summary |
| `/reports/attendance` | `GET` | Admin | Generate monthly attendance summary |
