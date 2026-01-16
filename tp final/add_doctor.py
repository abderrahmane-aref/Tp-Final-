import sqlite3
import os

def add_doctor():
    """إضافة طبيب جديد إلى قاعدة البيانات"""
    # الاتصال بقاعدة البيانات
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("=== add new doctor ===")
    
    # بيانات الطبيب الجديد
    username = input("اسم المستخدم للطبيب الجديد: ") or "nadir"
    password = input("كلمة المرور (افتراضي docpass123): ") or "ibiza"
    role = "Doctor"
    
    try:
        # التحقق من أن اسم المستخدم غير موجود
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
        if cursor.fetchone()[0] > 0:
            print("✗ اسم المستخدم موجود بالفعل! اختر اسم آخر.")
            return
        
        # إضافة الطبيب
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                      (username, password, role))
        
        # حفظ التغييرات
        user_id = cursor.lastrowid
        conn.commit()
        
        print("✓ تم إضافة الطبيب الجديد بنجاح!")
        print(f"  اسم المستخدم: {username}")
        print(f"  كلمة المرور: {password}")
        print(f"  الدور: {role}")
        print(f"  رقم المستخدم: {user_id}")
        
    except Exception as e:
        print(f"✗ حدث خطأ: {e}")
    finally:
        conn.close()

def list_doctors():
    """عرض جميع الأطباء المسجلين"""
    # الاتصال بقاعدة البيانات
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # جلب جميع الأطباء
        cursor.execute("SELECT id, username FROM users WHERE role = ?", ("Doctor",))
        doctors = cursor.fetchall()
        
        if doctors:
            print("\n=== الأطباء المسجلين ===")
            for doctor in doctors:
                print(f"  ID: {doctor[0]}, Username: {doctor[1]}")
        else:
            print("\n✗ لا يوجد أطباء مسجلين")
            
    except Exception as e:
        print(f"✗ حدث خطأ أثناء عرض الأطباء: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("helloooo")
    print("1. add new doctor  ")
    print("2. see all users  ")
    
    choice = input("اchoose  (1 أو 2): ")
    
    if choice == "1":
        add_doctor()
    elif choice == "2":
        list_doctors()
    else:
        print("false  !")