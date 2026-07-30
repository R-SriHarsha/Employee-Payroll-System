// -------- INDEX / EMPLOYEE SCRIPTS ---------


async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const res = await fetch("/employee_auth/login", {
        credentials: "include",
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    });

    if (res.ok) {
        window.location.href = "/employee.html";

    } else {
        alert("Invalid login");
    }
}

async function logout() {
    await fetch("/employee_auth/logout", { credentials: "include", method: "POST" });
    window.location.href = "/";
}


// -------- EMPLOYEE DASHBOARD SCRIPTS ---------
async function checkAuth() {
    const res = await fetch("/employee_auth/check");

    if (!res.ok) {
        // If not logged in and trying to access employee.html, redirect back to login
        if (window.location.pathname.includes("employee.html") || window.location.pathname.includes("payslip.html")) {
            window.location.href = "/";
        }
    } else {
        // If logged in and on index page, redirect to employee page
        if (window.location.pathname === "/" || window.location.pathname.includes("index.html")) {
            window.location.href = "/employee.html";
        }
    }
}

checkAuth();

let EMP_ID = null;


async function loadUser() {
    const res = await fetch("/employee_auth/me", {
        credentials: "include"
    });

    if (!res.ok) {
        return;
    }

    const data = await res.json();
    EMP_ID = data.employee_id;

    console.log("Logged in employee:", EMP_ID);
    const empIdSpan = document.getElementById("EMP_ID");
    if (empIdSpan) {
        empIdSpan.textContent = data.employee_id;
        loadProfile();
        loadHistoricalPay();
        loadEmployeeLeaves();
    }
}

loadUser();

async function loadProfile() {
    if (!EMP_ID) return;
    const res = await fetch(`/employees/${EMP_ID}`);
    const detailsDiv = document.getElementById("profileDetails");
    if (!detailsDiv) return;
    
    if (!res.ok) {
        detailsDiv.innerHTML = `<p class="empty" style="color:red;">Employee not found!</p>`;
        return;
    }
    const data = await res.json();
    detailsDiv.innerHTML = `
        <p><strong>Name:</strong> ${data.name}</p>
        <p><strong>Department:</strong> ${data.department}</p>
        <p><strong>Role:</strong> ${data.designation}</p>
        <p><strong>Base Salary:</strong> ${data.base_salary}</p>
    `;
}


async function loadHistoricalPay() {


    if (!EMP_ID) return;
    const res = await fetch(`/payroll/${EMP_ID}`);
    const list = document.getElementById("paySlipsList");
    if (!res.ok) {
        list.innerHTML = `<li><span style="color:red;">Error fetching pay slips</span></li>`;
        return;
    }
    const data = await res.json();
    list.innerHTML = "";
    if (!Array.isArray(data) || data.length === 0) {
        list.innerHTML = "<li>No payroll data found for you</li>";
        return;
    }
    data.forEach(p => {
        const li = document.createElement("li");
        li.innerHTML = `<strong>${p.month}/${p.year}</strong> - Net: ${p.net_salary} 
        <button class="btn-small" style="background:#10b981; color:white; border:none; cursor:pointer;" onclick="openPayslip(${EMP_ID}, ${p.month}, ${p.year})">View Payslip</button>`;
        list.appendChild(li);
    });
}

// -------- EMPLOYEE LEAVES --------
async function submitLeaveRequest() {
    if (!EMP_ID) return;

    const payload = {
        employee_id: EMP_ID,
        start_date: document.getElementById("leaveStart").value,
        end_date: document.getElementById("leaveEnd").value,
        reason: document.getElementById("leaveReason").value
    };

    if (!payload.start_date || !payload.end_date) {
        alert("Please select both start and end dates.");
        return;
    }

    const res = await fetch("/leaves/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    if (res.ok) {
        alert("Leave request submitted!");
        document.getElementById("leaveStart").value = "";
        document.getElementById("leaveEnd").value = "";
        document.getElementById("leaveReason").value = "";
        loadEmployeeLeaves();
    } else {
        const data = await res.json();
        alert(data.error || "Failed to submit leave");
    }
}

async function loadEmployeeLeaves() {
    if (!EMP_ID) return;
    const res = await fetch(`/leaves/employee/${EMP_ID}`);
    const list = document.getElementById("leaveList");
    if (!list) return;

    list.innerHTML = "";
    if (!res.ok) return;

    const data = await res.json();
    if (data.length === 0) {
        list.innerHTML = `<li class="empty">No leave requests found.</li>`;
        return;
    }

    data.forEach(l => {
        const li = document.createElement("li");
        let statusColor = "gray";
        if (l.status === "Approved") statusColor = "green";
        if (l.status === "Rejected") statusColor = "red";

        li.innerHTML = `
            <div><strong>${l.start_date} to ${l.end_date}</strong>: ${l.reason}</div>
            <div style="color:${statusColor}; font-weight:bold;">${l.status}</div>
        `;
        list.appendChild(li);
    });
}

// -------- ADMIN DASHBOARD SCRIPTS ---------

async function checkAdminAuth() {
    if (!window.location.pathname.includes("admin.html")) return;

    const res = await fetch("/auth/check");
    if (res.ok) {
        document.getElementById("loginGate").classList.add("hidden");
        document.getElementById("dashboard").classList.remove("hidden");
        loadAdminData();
    } else {
        document.getElementById("loginGate").classList.remove("hidden");
        document.getElementById("dashboard").classList.add("hidden");
    }
}

checkAdminAuth();

async function adminLogin() {
    const user = document.getElementById("adminUser").value;
    const pass = document.getElementById("adminPass").value;

    const res = await fetch("/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: user, password: pass })
    });

    if (res.ok) {
        document.getElementById("loginGate").classList.add("hidden");
        document.getElementById("dashboard").classList.remove("hidden");
        loadAdminData();
    } else {
        document.getElementById("adminError").innerText = "Invalid credentials";
    }
}

async function adminLogout() {
    await fetch("/auth/logout", { method: "POST" });
    document.getElementById("loginGate").classList.remove("hidden");
    document.getElementById("dashboard").classList.add("hidden");
    document.getElementById("adminUser").value = "";
    document.getElementById("adminPass").value = "";
}

async function loadAdminData() {
    const res = await fetch("/employees/");
    const data = await res.json();
    const tbody = document.getElementById("empTableBody");
    tbody.innerHTML = "";
    data.forEach(emp => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${emp.id}</td>
            <td>${emp.name}</td>
            <td>${emp.department}</td>
            <td>${emp.designation}</td>
            <td>${emp.base_salary}</td>
            <td>
                <button class="btn-small edit-btn" onclick="editEmployee(${emp.id}, '${emp.name}', '${emp.department}', '${emp.designation}', ${emp.base_salary})">Edit</button>
                <button class="btn-small del-btn" onclick="deleteEmployee(${emp.id})">Del</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
    getPayrolls();
}

let editingId = null;

async function addEmployee() {
    const payload = {
        name: document.getElementById("empName").value,
        department: document.getElementById("empDept").value,
        designation: document.getElementById("empRole").value,
        base_salary: Number(document.getElementById("empSalary").value),
        password: document.getElementById("empPassword").value
    };

    const url = editingId ? `/employees/${editingId}` : "/employees/";
    const method = editingId ? "PUT" : "POST";

    const res = await fetch(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    editingId = null;
    document.getElementById("empName").value = "";
    document.getElementById("empDept").value = "";
    document.getElementById("empRole").value = "";
    document.getElementById("empSalary").value = "";
    document.getElementById("empPassword").value = "";

    let btn = document.querySelector(".card button[onclick='addEmployee()']");
    if (btn) btn.innerText = "Save Employee";
    const data = await res.json();

    loadAdminData();


}

function editEmployee(id, name, dept, role, salary) {
    editingId = id;
    document.getElementById("empName").value = name;
    document.getElementById("empDept").value = dept;
    document.getElementById("empRole").value = role;
    document.getElementById("empSalary").value = salary;
    document.getElementById("empPassword").value = "";

    let btn = document.querySelector(".card button[onclick='addEmployee()']");
    if (btn) btn.innerText = "Update Employee " + id;
}

async function deleteEmployee(id) {
    if (!confirm("Are you sure you want to delete employee " + id + "?")) return;
    await fetch(`/employees/${id}`, { method: "DELETE" });
    loadAdminData();
}

async function recordAttendance() {
    const payload = {
        employee_id: Number(document.getElementById("attEmpId").value),
        month: Number(document.getElementById("attMonth").value),
        year: Number(document.getElementById("attYear").value),
        present_days: Number(document.getElementById("attPresentDays").value),
        leaves: Number(document.getElementById("attLeaves").value)
    };

    if (!payload.employee_id || !payload.month || !payload.year) {
        alert("Please provide Employee ID, Month, and Year");
        return;
    }

    const res = await fetch("/attendance/monthly", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    if (res.ok) {
        alert("Monthly attendance recorded successfully");
    } else {
        const data = await res.json();
        alert(data.error || "Failed to record attendance");
    }
}

async function runPayroll() {
    const empId = document.getElementById("payEmpId").value;
    const month = document.getElementById("payMonth").value;
    const year = document.getElementById("payYear").value;

    if (!empId || !month || !year) {
        alert("Please fill all fields");
        return;
    }

    const res = await fetch(`/payroll/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            employee_id: Number(empId),
            month: Number(month),
            year: Number(year)
        })
    });

    const data = await res.json();

    if (res.ok) {
        alert(data.message);
        getPayrolls(); // refresh list
    } else {
        alert(data.error || "Payroll failed");
    }

}



async function getPayrolls() {
    const res = await fetch("/payroll/");
    if (!res.ok) return;
    const data = await res.json();
    const list = document.getElementById("payList");
    list.innerHTML = "";

    if (!Array.isArray(data) || data.length === 0) {
        list.innerHTML = "<li><span style='color:gray;'>No payroll runs found</span></li>";
        return;
    }

    data.forEach(p => {
        const li = document.createElement("li");
        li.innerHTML = `
            <span style="font-size:14px;">Emp ID: ${p.employee_id} | ${p.month}/${p.year} | Net: ${p.net_salary}</span>
            <button onclick="openPayslip(${p.employee_id}, ${p.month}, ${p.year})">
    View Payslip
</button>

        `;
        list.appendChild(li);
    });
}

async function openPayslip(empId, month, year) {
    try {
        const res = await fetch(`/payroll/${empId}/download/${month}/${year}`);
        
        if (!res.ok) {
            alert("Payslip not found!");
            return;
        }

        const data = await res.json();
        localStorage.setItem("payslipData", JSON.stringify(data));
        window.open("/payslip.html", "_blank");

    } catch (error) {
        console.error(error);
        alert("Failed to load payslip");
    }
}

function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll(".section").forEach(sec => {
        sec.classList.add("hidden");
    });

    // Show selected section
    document.getElementById(sectionId).classList.remove("hidden");

    // Update active menu
    document.querySelectorAll(".sidebar ul li").forEach(item => {
        item.classList.remove("active");
    });

    event.target.classList.add("active");
    
    if (sectionId === "leaves") {
        loadAdminLeaves();
    }
}

// -------- ADMIN LEAVES --------
async function loadAdminLeaves() {
    const res = await fetch("/leaves/");
    const tbody = document.getElementById("adminLeaveTableBody");
    if (!tbody) return;

    tbody.innerHTML = "";
    if (!res.ok) return;

    const data = await res.json();
    data.forEach(l => {
        const tr = document.createElement("tr");
        
        // Status actions
        let actionButtons = "";
        if (l.status === "Pending") {
            actionButtons = `
                <button class="btn-small edit-btn" onclick="updateLeaveStatus(${l.id}, 'Approved')" style="background:#22c55e;">Approve</button>
                <button class="btn-small del-btn" onclick="updateLeaveStatus(${l.id}, 'Rejected')">Reject</button>
            `;
        } else {
            actionButtons = `<em>Admin ${l.status}</em>`;
        }

        tr.innerHTML = `
            <td>${l.id}</td>
            <td>${l.employee_id}</td>
            <td>${l.start_date}</td>
            <td>${l.end_date}</td>
            <td>${l.reason}</td>
            <td><strong>${l.status}</strong></td>
            <td>${actionButtons}</td>
        `;
        tbody.appendChild(tr);
    });
}

async function updateLeaveStatus(leaveId, status) {
    const res = await fetch(`/leaves/${leaveId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: status })
    });

    if (res.ok) {
        loadAdminLeaves();
    } else {
        alert("Failed to update leave status");
    }
}


async function getPayrollReport() {
    const month = document.getElementById("reportMonth").value;
    const year = document.getElementById("reportYear").value;

    const res = await fetch(`/reports/payroll?month=${month}&year=${year}`);
    const data = await res.json();

    const list = document.getElementById("reportList");
    list.innerHTML = "";

    data.data.forEach(r => {
        const li = document.createElement("li");
        li.innerText = `${r.name} - ₹${r.net_salary}`;
        list.appendChild(li);
    });

    const total = document.createElement("li");
    total.innerHTML = `<strong>Total Salary: ₹${data.total_salary}</strong>`;
    list.appendChild(total);
}


async function getAttendanceReport() {
    const month = document.getElementById("reportMonth").value;
    const year = document.getElementById("reportYear").value;

    const res = await fetch(`/reports/attendance?month=${month}&year=${year}`);
    const data = await res.json();

    const list = document.getElementById("reportList");
    list.innerHTML = "";

    data.forEach(r => {
        const li = document.createElement("li");
        li.innerText = `${r.name} - Present: ${r.present_days}, Leaves: ${r.leaves}`;
        list.appendChild(li);
    });
}

