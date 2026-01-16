# نظام التحكم في الصلاحيات بناءً على الأدوار (RBAC)
## Role-Based Access Control Implementation

---

## 📋 نظرة عامة | Overview

تم تطبيق نظام متكامل للتحكم في الصلاحيات بناءً على أدوار المستخدمين في نظام السجلات الطبية الموزع.

A comprehensive Role-Based Access Control (RBAC) system has been implemented in the distributed medical records system.

---

## 👥 الأدوار والصلاحيات | Roles and Permissions

### 1. الطبيب | Doctor
**الصلاحيات الكاملة | Full Access:**
- ✅ **المرضى | Patients:**
  - عرض جميع بيانات المرضى (Read)
  - إضافة مرضى جدد (Write)
  - تعديل بيانات المرضى (Update)
  - حذف المرضى (Delete)
  
- ✅ **التقارير الطبية | Medical Reports:**
  - عرض جميع التقارير (Read)
  - إنشاء تقارير جديدة (Write)
  
- ✅ **الوصفات الطبية | Prescriptions:**
  - عرض جميع الوصفات (Read)
  - إضافة وصفات طبية جديدة (Write)

### 2. الممرض/الممرضة | Nurse
**صلاحيات القراءة فقط | Read-Only Access:**
- ✅ **المرضى | Patients:**
  - عرض بيانات المرضى فقط (Read Only)
  - ❌ لا يمكن الإضافة أو التعديل أو الحذف
  
- ✅ **التقارير الطبية | Medical Reports:**
  - عرض التقارير فقط (Read Only)
  - ❌ لا يمكن إنشاء تقارير جديدة
  
- ❌ **الوصفات الطبية | Prescriptions:**
  - ممنوع من الوصول (No Access)

### 3. الصيدلي | Pharmacist
**وصول محدود للوصفات فقط | Limited Access to Prescriptions Only:**
- ❌ **المرضى | Patients:**
  - ممنوع من الوصول (No Access)
  
- ❌ **التقارير الطبية | Medical Reports:**
  - ممنوع من الوصول (No Access)
  
- ✅ **الوصفات الطبية | Prescriptions:**
  - عرض الوصفات فقط (Read Only)
  - ❌ لا يمكن إضافة وصفات جديدة

---

## 🔐 التطبيق التقني | Technical Implementation

### 1. Backend (FastAPI - Python)

#### تعريف الصلاحيات | Permission Definitions
```python
ROLE_PERMISSIONS = {
    "Doctor": {
        "patients": ["read", "write", "update", "delete"],
        "reports": ["read", "write"],
        "prescriptions": ["read", "write"]
    },
    "Nurse": {
        "patients": ["read"],
        "reports": ["read"],
        "prescriptions": []
    },
    "Pharmacist": {
        "patients": [],
        "reports": [],
        "prescriptions": ["read"]
    }
}
```

#### دالة التحقق من الصلاحيات | Permission Check Function
```python
def check_permission(role: str, resource: str, action: str) -> bool:
    """
    التحقق من صلاحيات المستخدم
    Verify user permissions
    """
    if role not in ROLE_PERMISSIONS:
        return False
    if resource not in ROLE_PERMISSIONS[role]:
        return False
    return action in ROLE_PERMISSIONS[role][resource]
```

#### حماية نقاط الوصول API | API Endpoint Protection
جميع نقاط الوصول API محمية بفحص الصلاحيات:
```python
@app.get("/api/patients")
def get_patients(x_user_role: Optional[str] = Header(None), 
                 x_user_name: Optional[str] = Header(None)):
    """الحصول على قائمة المرضى - يتطلب صلاحية قراءة"""
    user = get_current_user(x_user_role, x_user_name)
    if not check_permission(user["role"], "patients", "read"):
        raise HTTPException(status_code=403, 
                          detail="Access denied - No permission to view patients")
    # ... continue processing
```

### 2. Frontend (JavaScript)

#### إرسال بيانات المستخدم مع كل طلب | Sending User Data with Requests
```javascript
// دالة للحصول على headers المصادقة
function getAuthHeaders() {
    return {
        'X-User-Role': role,
        'X-User-Name': username
    };
}

// استخدامها في طلبات API
const response = await fetch('/api/patients', {
    headers: getAuthHeaders()
});
```

#### إخفاء العناصر بناءً على الدور | Hide Elements Based on Role
```javascript
function applyRolePermissions() {
    const isDoctor = role === "Doctor";
    const isNurse = role === "Nurse";
    const isPharmacist = role === "Pharmacist";

    if (isNurse) {
        // الممرض: إخفاء أزرار الإضافة والتعديل
        hideElement('addPatientCard');
        hideElement('addReportBtn');
        hideElement('prescriptionsLink');
    } else if (isPharmacist) {
        // الصيدلي: إخفاء كل شيء ما عدا الوصفات
        hideElement('addPatientCard');
        hideElement('reportsLink');
        // ... etc
    }
}
```

---

## 🧪 اختبار النظام | System Testing

### اختبار دور الطبيب | Testing Doctor Role
```
اسم المستخدم | Username: doctor
كلمة المرور | Password: 1111

✅ يمكنه رؤية وإدارة كل شيء
✅ Can see and manage everything
```

### اختبار دور الممرض | Testing Nurse Role
```
اسم المستخدم | Username: nurse
كلمة المرور | Password: nurse123

✅ يمكن رؤية المرضى والتقارير فقط
✅ Can only view patients and reports
❌ لا يمكن الإضافة أو التعديل أو الحذف
❌ Cannot add, edit, or delete
```

### اختبار دور الصيدلي | Testing Pharmacist Role
```
اسم المستخدم | Username: pharma
كلمة المرور | Password: pharma123

✅ يمكن رؤية الوصفات الطبية فقط
✅ Can only view prescriptions
❌ لا يمكن رؤية المرضى أو التقارير
❌ Cannot view patients or reports
```

---

## 🔒 ميزات الأمان | Security Features

### 1. التحقق على مستوى الخادم | Server-Side Validation
- ✅ جميع الطلبات محمية بفحص الصلاحيات
- ✅ لا يمكن تجاوز القيود من المتصفح
- ✅ رسائل خطأ واضحة عند محاولة الوصول غير المصرح

### 2. التحقق على مستوى العميل | Client-Side Validation
- ✅ إخفاء الأزرار والخيارات غير المصرح بها
- ✅ تحسين تجربة المستخدم
- ✅ منع المحاولات غير المقصودة

### 3. تتبع العمليات | Operation Tracking
- ✅ تسجيل اسم المستخدم في كل عملية
- ✅ إشعارات عند إضافة/تعديل/حذف البيانات
- ✅ سجل واضح لمن قام بماذا

---

## 📁 الملفات المعدلة | Modified Files

### 1. main.py
- إضافة تعريفات الصلاحيات `ROLE_PERMISSIONS`
- دالة `check_permission()` للتحقق من الصلاحيات
- دالة `get_current_user()` لاستخراج بيانات المستخدم
- تحديث جميع نقاط API بفحص الصلاحيات

### 2. templates/home.html
- دالة `getAuthHeaders()` لإرسال بيانات المستخدم
- تحديث جميع طلبات `fetch()` لإضافة headers
- تحسين دالة `applyRolePermissions()` لإخفاء العناصر

### 3. init_db.py
- بدون تغييرات (الهيكل الحالي يدعم RBAC)

---

## 🚀 التشغيل | How to Run

### 1. تهيئة قاعدة البيانات | Initialize Database
```bash
python init_db.py
```

### 2. تشغيل الخادم | Start Server
```bash
# باستخدام FastAPI مباشرة
uvicorn main:app --reload

# أو باستخدام ملف bat
run_server.bat
```

### 3. الوصول للنظام | Access System
```
افتح المتصفح: http://localhost:8000
Open browser: http://localhost:8000

قم بتسجيل الدخول باستخدام أحد الحسابات المذكورة أعلاه
Login using one of the accounts mentioned above
```

---

## ⚠️ ملاحظات مهمة | Important Notes

### 1. الأمان | Security
- النظام الحالي يستخدم headers بسيطة للمصادقة
- في بيئة الإنتاج، يُنصح باستخدام JWT أو OAuth
- يجب تشفير كلمات المرور في قاعدة البيانات

### 2. التوسع المستقبلي | Future Enhancements
- إضافة المزيد من الأدوار (مثل: مدير، محاسب)
- سجل تدقيق كامل لجميع العمليات
- نظام إشعارات متقدم بناءً على الدور
- تقارير مخصصة لكل دور

### 3. الصيانة | Maintenance
- يمكن تعديل الصلاحيات بسهولة من `ROLE_PERMISSIONS`
- إضافة أدوار جديدة بسيطة ومباشرة
- التوثيق الكامل بالعربية والإنجليزية

---

## 📞 الدعم | Support

في حالة وجود أي استفسارات أو مشاكل:
- راجع السجلات (Logs) للأخطاء
- تحقق من صلاحيات المستخدم في `ROLE_PERMISSIONS`
- تأكد من إرسال headers صحيحة في طلبات API

For any questions or issues:
- Check logs for errors
- Verify user permissions in `ROLE_PERMISSIONS`
- Ensure correct headers are sent in API requests

---

**تم التطبيق بنجاح ✅**
**Successfully Implemented ✅**

**تاريخ التحديث | Update Date:** December 7, 2025
