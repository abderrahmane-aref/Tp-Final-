from fastapi import FastAPI, Form, Request, HTTPException, Header, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
import sqlite3
import os
from datetime import datetime

# Import our new middleware
from middleware.auth_middleware import AuthMiddleware

app = FastAPI()

# Add our custom middleware
def add_middleware(app):
    app.add_middleware(AuthMiddleware)

# Add middleware to the app
add_middleware(app)

# Database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

# static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# templates folder
templates = Jinja2Templates(directory="templates")

# التحكم في الصلاحيات بناءً على الأدوار - Role-Based Access Control (RBAC)
# تعريف الأدوار والصلاحيات المسموحة لكل دور
ROLE_PERMISSIONS = {
    "Doctor": {
        "patients": ["read", "write", "update", "delete"],  # طبيب: كامل الصلاحيات على المرضى
        "reports": ["read", "write"],  # طبيب: قراءة وكتابة التقارير
        "prescriptions": ["read", "write"]  # طبيب: قراءة وكتابة الوصفات الطبية
    },
    "Nurse": {
        "patients": ["read"],  # ممرض/ة: قراءة فقط للمرضى
        "reports": ["read"],  # ممرض/ة: قراءة فقط للتقارير
        "prescriptions": []  # ممرض/ة: ممنوع من الوصول للوصفات الطبية
    },
    "Pharmacist": {
        "patients": ["read"],  # صيدلي: قراءة فقط لبيانات المرضى
        "reports": [],  # صيدلي: ممنوع من الوصول للتقارير
        "prescriptions": ["read"]  # صيدلي: قراءة فقط للوصفات الطبية
    },
    "Admin": {
        "patients": ["read", "write", "update", "delete"],
        "reports": ["read", "write"],
        "prescriptions": ["read", "write"],
        "users": ["read", "write", "update", "delete"]
    }
}

# دالة للتحقق من صلاحيات المستخدم - Check user permissions
def check_permission(role: str, resource: str, action: str) -> bool:
    """
    التحقق من صلاحيات المستخدم للقيام بعملية معينة
    Verify if user role has permission to perform action on resource
    
    Args:
        role: دور المستخدم (Doctor/Nurse/Pharmacist)
        resource: المورد المطلوب (patients/reports/prescriptions)
        action: العملية المطلوبة (read/write/update/delete)
    
    Returns:
        True إذا كان المستخدم لديه الصلاحية، False خلاف ذلك
    """
    if role not in ROLE_PERMISSIONS:
        return False
    
    if resource not in ROLE_PERMISSIONS[role]:
        return False
    
    return action in ROLE_PERMISSIONS[role][resource]

# دالة للحصول على بيانات المستخدم من الهيدر
def get_current_user(x_user_role: Optional[str] = Header(None), 
                      x_user_name: Optional[str] = Header(None)) -> dict:
    """
    الحصول على معلومات المستخدم الحالي من الهيدر
    Get current user information from request headers
    """
    if not x_user_role or not x_user_name:
        raise HTTPException(status_code=401, detail="Unauthorized - No user credentials")
    
    return {"role": x_user_role, "username": x_user_name}

# ============================================
# TIER 3: DATA LAYER (Database Operations)
# ============================================
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def verify_user(username: str, password: str):
    """Data Tier: Verify user credentials"""
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password)
    ).fetchone()
    conn.close()
    return dict(user) if user else None

def get_all_patients():
    """Data Tier: Get all patients from database"""
    conn = get_db_connection()
    patients = conn.execute("SELECT * FROM patients ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(patient) for patient in patients]

def add_patient_to_db(first_name, last_name, dob, sex, notes):
    """Data Tier: Add patient to database"""
    conn = get_db_connection()
    visit_date = datetime.now().strftime("%Y-%m-%d")
    cursor = conn.execute(
        "INSERT INTO patients (first_name, last_name, dob, sex, last_visit, visit_place, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (first_name, last_name, dob, sex, visit_date, "Clinic", notes)
    )
    patient_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return patient_id

def add_notification(title, message):
    """Data Tier: Add notification to database"""
    conn = get_db_connection()
    cursor = conn.execute(
        "INSERT INTO notifications (title, message) VALUES (?, ?)",
        (title, message)
    )
    notification_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return notification_id

def get_all_notifications():
    """Data Tier: Get all notifications from database"""
    conn = get_db_connection()
    notifications = conn.execute("SELECT * FROM notifications ORDER BY created_at DESC LIMIT 20").fetchall()
    conn.close()
    return [dict(notif) for notif in notifications]

def get_unread_notifications_count():
    """Data Tier: Get count of unread notifications"""
    conn = get_db_connection()
    result = conn.execute("SELECT COUNT(*) as count FROM notifications WHERE is_read = 0").fetchone()
    conn.close()
    return result['count'] if result else 0

def mark_notification_as_read(notification_id):
    """Data Tier: Mark notification as read"""
    conn = get_db_connection()
    conn.execute("UPDATE notifications SET is_read = 1 WHERE id = ?", (notification_id,))
    conn.commit()
    conn.close()
    return True

def update_patient_in_db(patient_id, first_name, last_name, dob, sex, notes):
    """Data Tier: Update patient in database"""
    conn = get_db_connection()
    conn.execute(
        "UPDATE patients SET first_name = ?, last_name = ?, dob = ?, sex = ?, notes = ? WHERE id = ?",
        (first_name, last_name, dob, sex, notes, patient_id)
    )
    conn.commit()
    conn.close()
    return True

def delete_patient_from_db(patient_id):
    """Data Tier: Delete patient from database"""
    conn = get_db_connection()
    conn.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
    conn.commit()
    conn.close()
    return True

def get_patient_by_id(patient_id):
    """Data Tier: Get single patient by ID"""
    conn = get_db_connection()
    patient = conn.execute("SELECT * FROM patients WHERE id = ?", (patient_id,)).fetchone()
    conn.close()
    return dict(patient) if patient else None

def get_statistics():
    """Data Tier: Get system statistics for reports"""
    conn = get_db_connection()
    
    # Total patients
    total_patients = conn.execute("SELECT COUNT(*) as count FROM patients").fetchone()['count']
    
    # Patients by gender
    male_count = conn.execute("SELECT COUNT(*) as count FROM patients WHERE sex = 'Male'").fetchone()['count']
    female_count = conn.execute("SELECT COUNT(*) as count FROM patients WHERE sex = 'Female'").fetchone()['count']
    
    # Recent patients (last 7 days)
    recent = conn.execute(
        "SELECT COUNT(*) as count FROM patients WHERE last_visit >= date('now', '-7 days')"
    ).fetchone()['count']
    
    conn.close()
    return {
        'total_patients': total_patients,
        'male_patients': male_count,
        'female_patients': female_count,
        'recent_visits': recent
    }

# ==============================
# User Management Functions
# ==============================

def get_all_users():
    """Get all users from database"""
    conn = get_db_connection()
    users = conn.execute("SELECT id, username, role FROM users ORDER BY id").fetchall()
    conn.close()
    return [dict(user) for user in users]

def add_user_to_db(username, password, role):
    """Add new user to database"""
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, password, role)
        )
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        conn.close()
        raise Exception("Username already exists")

def delete_user_from_db(user_id):
    """Delete user from database"""
    conn = get_db_connection()
    # Prevent deleting the admin user
    admin_check = conn.execute("SELECT role FROM users WHERE id = ?", (user_id,)).fetchone()
    if admin_check and admin_check['role'] == 'Admin':
        conn.close()
        raise Exception("Cannot delete admin user")
    
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return True


def get_all_reports():
    """Data Tier: Get all reports from database"""
    conn = get_db_connection()
    reports = conn.execute("""
        SELECT r.*, p.first_name, p.last_name 
        FROM reports r 
        JOIN patients p ON r.patient_id = p.id 
        ORDER BY r.created_at DESC
    """).fetchall()
    conn.close()
    return [dict(report) for report in reports]

def add_report_to_db(patient_id, report_type, diagnosis, treatment, medications, notes, created_by):
    """Data Tier: Add report to database"""
    conn = get_db_connection()
    cursor = conn.execute(
        "INSERT INTO reports (patient_id, report_type, diagnosis, treatment, medications, notes, created_by) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (patient_id, report_type, diagnosis, treatment, medications, notes, created_by)
    )
    report_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return report_id

def get_all_prescriptions():
    """Data Tier: Get all prescriptions from database"""
    conn = get_db_connection()
    prescriptions = conn.execute("""
        SELECT p.*, pt.first_name, pt.last_name 
        FROM prescriptions p 
        JOIN patients pt ON p.patient_id = pt.id 
        ORDER BY p.created_at DESC
    """).fetchall()
    conn.close()
    return [dict(prescription) for prescription in prescriptions]

def add_prescription_to_db(patient_id, medication_name, dosage, frequency, duration, instructions, prescribed_by):
    """Data Tier: Add prescription to database"""
    conn = get_db_connection()
    cursor = conn.execute(
        "INSERT INTO prescriptions (patient_id, medication_name, dosage, frequency, duration, instructions, prescribed_by) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (patient_id, medication_name, dosage, frequency, duration, instructions, prescribed_by)
    )
    prescription_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return prescription_id

# ============================================
# TIER 2: BUSINESS LOGIC LAYER
# ============================================
def validate_patient_data(first_name, last_name, dob, sex):
    """Business Tier: Validate patient data"""
    if not first_name or not last_name:
        return False, "First name and last name are required"
    if not dob:
        return False, "Date of birth is required"
    if sex not in ["Male", "Female"]:
        return False, "Invalid gender"
    return True, "Valid"

def process_patient_registration(first_name, last_name, dob, sex, notes):
    """Business Tier: Process patient registration"""
    # Validate data
    is_valid, message = validate_patient_data(first_name, last_name, dob, sex)
    if not is_valid:
        return {"success": False, "message": message}
    
    # Save to database
    try:
        patient_id = add_patient_to_db(first_name, last_name, dob, sex, notes)
        
        # Create notification for new patient
        notification_title = "New Patient Added"
        notification_message = f"Patient {first_name} {last_name} has been successfully registered (ID: {patient_id})"
        add_notification(notification_title, notification_message)
        
        return {
            "success": True,
            "message": "Patient registered successfully",
            "patient_id": patient_id
        }
    except Exception as e:
        return {"success": False, "message": str(e)}

# ============================================
# TIER 1: PRESENTATION LAYER (API Endpoints)
# ============================================
@app.get("/", response_class=HTMLResponse)
def show_login(request: Request):
    """Presentation Tier: Show login page"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    """Presentation Tier: Handle login"""
    user = verify_user(username, password)
    if user:
        return JSONResponse({
            "success": True,
            "message": "Login successful",
            "user": {
                "username": user["username"],
                "role": user["role"]
            }
        })
    return JSONResponse({"success": False, "message": "Invalid credentials"}, status_code=401)

@app.get("/home", response_class=HTMLResponse)
def show_home(request: Request):
    """Presentation Tier: Show home page"""
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/api/patients")
def get_patients(request: Request):
    """
    Presentation Tier: Get all patients (API endpoint)
    الحصول على قائمة المرضى - يتطلب صلاحية قراءة
    """
    # التحقق من صلاحية القراءة - Check read permission
    user = request.scope.get("user", {})
    if not user or not check_permission(user["role"], "patients", "read"):
        raise HTTPException(status_code=403, detail="Access denied - No permission to view patients")
    
    patients = get_all_patients()
    return JSONResponse({"success": True, "data": patients})

@app.post("/api/patients")
def create_patient(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    dob: str = Form(...),
    sex: str = Form(...),
    notes: str = Form(""),
):
    """
    Presentation Tier: Create new patient
    إضافة مريض جديد - يتطلب صلاحية كتابة
    """
    # التحقق من صلاحية الكتابة - Check write permission
    user = request.scope.get("user", {})
    if not user or not check_permission(user["role"], "patients", "write"):
        raise HTTPException(status_code=403, detail="Access denied - No permission to add patients")
    
    result = process_patient_registration(first_name, last_name, dob, sex, notes)
    if result["success"]:
        return JSONResponse(result)
    return JSONResponse(result, status_code=400)

@app.get("/api/notifications")
def get_notifications():
    """Presentation Tier: Get all notifications"""
    notifications = get_all_notifications()
    unread_count = get_unread_notifications_count()
    return JSONResponse({
        "success": True, 
        "data": notifications,
        "unread_count": unread_count
    })

@app.post("/api/notifications/{notification_id}/read")
def mark_notification_read(notification_id: int):
    """Presentation Tier: Mark notification as read"""
    result = mark_notification_as_read(notification_id)
    return JSONResponse({"success": result})

@app.get("/api/patients/{patient_id}")
def get_patient(patient_id: int, request: Request):
    """
    Presentation Tier: Get patient by ID
    الحصول على بيانات مريض محدد - يتطلب صلاحية قراءة
    """
    # التحقق من صلاحية القراءة - Check read permission
    user = request.scope.get("user", {})
    if not user or not check_permission(user["role"], "patients", "read"):
        raise HTTPException(status_code=403, detail="Access denied - No permission to view patient details")
    
    patient = get_patient_by_id(patient_id)
    if patient:
        return JSONResponse({"success": True, "data": patient})
    return JSONResponse({"success": False, "message": "Patient not found"}, status_code=404)

@app.put("/api/patients/{patient_id}")
async def update_patient(
    patient_id: int,
    request: Request,
):
    """
    Presentation Tier: Update patient
    تحديث بيانات مريض - يتطلب صلاحية تحديث
    """
    # التحقق من صلاحية التحديث - Check update permission
    user = request.scope.get("user", {})
    if not user or not check_permission(user["role"], "patients", "update"):
        raise HTTPException(status_code=403, detail="Access denied - No permission to update patients")
    
    form = await request.form()
    first_name = form.get("first_name")
    last_name = form.get("last_name")
    dob = form.get("dob")
    sex = form.get("sex")
    notes = form.get("notes", "")
    
    # Validate
    is_valid, message = validate_patient_data(first_name, last_name, dob, sex)
    if not is_valid:
        return JSONResponse({"success": False, "message": message}, status_code=400)
    
    # Update
    try:
        update_patient_in_db(patient_id, first_name, last_name, dob, sex, notes)
        add_notification("Patient Updated", f"Patient {first_name} {last_name} (ID: {patient_id}) has been updated")
        return JSONResponse({"success": True, "message": "Patient updated successfully"})
    except Exception as e:
        return JSONResponse({"success": False, "message": str(e)}, status_code=400)

@app.delete("/api/patients/{patient_id}")
def delete_patient(patient_id: int, request: Request):
    """
    Presentation Tier: Delete patient
    حذف مريض - يتطلب صلاحية حذف
    """
    # التحقق من صلاحية الحذف - Check delete permission
    user = request.scope.get("user", {})
    if not user or not check_permission(user["role"], "patients", "delete"):
        raise HTTPException(status_code=403, detail="Access denied - No permission to delete patients")
    
    try:
        patient = get_patient_by_id(patient_id)
        if patient:
            delete_patient_from_db(patient_id)
            add_notification("Patient Deleted", f"Patient {patient['first_name']} {patient['last_name']} (ID: {patient_id}) has been deleted")
            return JSONResponse({"success": True, "message": "Patient deleted successfully"})
        return JSONResponse({"success": False, "message": "Patient not found"}, status_code=404)
    except Exception as e:
        return JSONResponse({"success": False, "message": str(e)}, status_code=400)

@app.get("/api/reports")
def get_reports(request: Request):
    """
    Presentation Tier: Get all reports
    الحصول على قائمة التقارير - يتطلب صلاحية قراءة
    """
    # التحقق من صلاحية القراءة - Check read permission
    user = request.scope.get("user", {})
    if not user or not check_permission(user["role"], "reports", "read"):
        raise HTTPException(status_code=403, detail="Access denied - No permission to view reports")
    
    reports = get_all_reports()
    return JSONResponse({"success": True, "data": reports})

@app.post("/api/reports")
async def create_report(request: Request):
    """
    Presentation Tier: Create new report
    إنشاء تقرير طبي جديد - يتطلب صلاحية كتابة
    """
    # التحقق من صلاحية الكتابة - Check write permission
    user = request.scope.get("user", {})
    if not user or not check_permission(user["role"], "reports", "write"):
        raise HTTPException(status_code=403, detail="Access denied - Only doctors can create reports")
    
    form = await request.form()
    patient_id = form.get("patient_id")
    report_type = form.get("report_type")
    diagnosis = form.get("diagnosis", "")
    treatment = form.get("treatment", "")
    medications = form.get("medications", "")
    notes = form.get("notes", "")
    created_by = form.get("created_by", "")
    
    try:
        report_id = add_report_to_db(patient_id, report_type, diagnosis, treatment, medications, notes, created_by)
        patient = get_patient_by_id(int(patient_id))
        add_notification("New Report Created", f"New {report_type} report created for patient {patient['first_name']} {patient['last_name']}")
        return JSONResponse({"success": True, "message": "Report created successfully", "report_id": report_id})
    except Exception as e:
        return JSONResponse({"success": False, "message": str(e)}, status_code=400)

# ==============================
# Admin User Management APIs
# ==============================

@app.get("/admin/users", response_class=HTMLResponse)
async def admin_users_page(request: Request):
    """Admin page to manage users"""
    # Get user from request scope (set by middleware)
    user = request.scope.get("user", {})
    
    # Check if user is admin
    if not user or user["role"] != "Admin":
        # Instead of raising an exception, redirect to login page
        return RedirectResponse(url="/login", status_code=303)
    
    # Return the admin users page without pre-loading users
    return templates.TemplateResponse("admin_users.html", {"request": request, "current_user": user})

@app.get("/api/admin/users")
async def get_users_api(request: Request):
    """API to get all users"""
    # Get user from request scope (set by middleware)
    user = request.scope.get("user", {})
    
    # Check if user is admin
    if not user or user.get("role") != "Admin":
        raise HTTPException(status_code=403, detail="Access denied - Admin only")
    
    # Get all users except admin
    all_users = get_all_users()
    users = [u for u in all_users if u["role"] != "Admin"]
    return JSONResponse({"success": True, "data": users})

@app.post("/api/admin/users")
async def add_user_api(request: Request, 
                      username: str = Form(...), 
                      password: str = Form(...), 
                      role: str = Form(...)):
    """API to add new user"""
    # Get user from request scope (set by middleware)
    user = request.scope.get("user", {})
    
    # Check if user is admin
    if not user or user.get("role") != "Admin":
        raise HTTPException(status_code=403, detail="Access denied - Admin only")
    
    # Validate role
    valid_roles = ["Doctor", "Nurse", "Pharmacist"]
    if role not in valid_roles:
        return JSONResponse({"success": False, "message": "Invalid role"}, status_code=400)
    
    # Check if username already exists
    existing_users = get_all_users()
    if any(u["username"] == username for u in existing_users):
        return JSONResponse({"success": False, "message": "Username already exists"}, status_code=400)
    
    try:
        user_id = add_user_to_db(username, password, role)
        return JSONResponse({"success": True, "message": "User added successfully", "user_id": user_id})
    except Exception as e:
        return JSONResponse({"success": False, "message": str(e)}, status_code=400)

@app.put("/api/admin/users/{user_id}")
async def update_user_api(user_id: int, request: Request, role: str = None):
    """API to update user role"""
    # Get user from request scope (set by middleware)
    user = request.scope.get("user", {})
    
    # Check if user is admin
    if not user or user.get("role") != "Admin":
        raise HTTPException(status_code=403, detail="Access denied - Admin only")
    
    # Get role from form data or JSON body
    if role is None:
        # Try to get role from JSON body
        try:
            body = await request.json()
            role = body.get("role")
        except:
            # If not JSON, try to get from form data
            form = await request.form()
            role = form.get("role")
    
    # Validate role
    valid_roles = ["Doctor", "Nurse", "Pharmacist"]
    if role not in valid_roles:
        return JSONResponse({"success": False, "message": "Invalid role"}, status_code=400)
    
    # Get the user to update
    target_user = None
    all_users = get_all_users()
    for u in all_users:
        if u["id"] == user_id:
            target_user = u
            break
    
    if not target_user:
        return JSONResponse({"success": False, "message": "User not found"}, status_code=404)
    
    # Prevent changing admin user
    if target_user["role"] == "Admin":
        return JSONResponse({"success": False, "message": "Cannot modify admin user"}, status_code=400)
    
    try:
        # Update user role in database
        conn = get_db_connection()
        conn.execute("UPDATE users SET role = ? WHERE id = ?", (role, user_id))
        conn.commit()
        conn.close()
        return JSONResponse({"success": True, "message": "User updated successfully"})
    except Exception as e:
        return JSONResponse({"success": False, "message": str(e)}, status_code=400)

@app.delete("/api/admin/users/{user_id}")
async def delete_user_api(user_id: int, request: Request):
    """API to delete user"""
    # Get user from request scope (set by middleware)
    user = request.scope.get("user", {})
    
    # Check if user is admin
    if not user or user.get("role") != "Admin":
        raise HTTPException(status_code=403, detail="Access denied - Admin only")
    
    # Prevent deletion of admin user
    target_user = None
    all_users = get_all_users()
    for u in all_users:
        if u["id"] == user_id:
            target_user = u
            break
    
    if not target_user:
        return JSONResponse({"success": False, "message": "User not found"}, status_code=404)
    
    if target_user["role"] == "Admin":
        return JSONResponse({"success": False, "message": "Cannot delete admin user"}, status_code=400)
    
    try:
        delete_user_from_db(user_id)
        return JSONResponse({"success": True, "message": "User deleted successfully"})
    except Exception as e:
        return JSONResponse({"success": False, "message": str(e)}, status_code=400)

@app.get("/api/prescriptions")
def get_prescriptions(request: Request):
    """
    Presentation Tier: Get all prescriptions
    الحصول على قائمة الوصفات الطبية - يتطلب صلاحية قراءة
    """
    # التحقق من صلاحية القراءة - Check read permission
    user = request.scope.get("user", {})
    if not user or not check_permission(user["role"], "prescriptions", "read"):
        raise HTTPException(status_code=403, detail="Access denied - No permission to view prescriptions")
    
    prescriptions = get_all_prescriptions()
    return JSONResponse({"success": True, "data": prescriptions})

@app.post("/api/prescriptions")
async def create_prescription(request: Request):
    """
    Presentation Tier: Create new prescription
    إضافة وصفة طبية جديدة - يتطلب صلاحية كتابة (للأطباء فقط)
    """
    # التحقق من صلاحية الكتابة - Check write permission
    user = request.scope.get("user", {})
    if not user or not check_permission(user["role"], "prescriptions", "write"):
        raise HTTPException(status_code=403, detail="Access denied - Only doctors can create prescriptions")
    
    form = await request.form()
    patient_id = form.get("patient_id")
    medication_name = form.get("medication_name")
    dosage = form.get("dosage")
    frequency = form.get("frequency")
    duration = form.get("duration")
    instructions = form.get("instructions", "")
    prescribed_by = form.get("prescribed_by", "")
    
    try:
        prescription_id = add_prescription_to_db(patient_id, medication_name, dosage, frequency, duration, instructions, prescribed_by)
        patient = get_patient_by_id(int(patient_id))
        add_notification("New Prescription Added", f"New prescription for {medication_name} added for patient {patient['first_name']} {patient['last_name']}")
        return JSONResponse({"success": True, "message": "Prescription added successfully", "prescription_id": prescription_id})
    except Exception as e:
        return JSONResponse({"success": False, "message": str(e)}, status_code=400)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
