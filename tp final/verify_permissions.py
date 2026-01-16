"""
Permission Verification Script
Verifies that role-based access control is configured correctly
"""

# Import the permissions from main.py
import sys
sys.path.insert(0, r"c:\Users\AREF ABDERAHMAN\Desktop\tp final")

from main import ROLE_PERMISSIONS, check_permission

def verify_permissions():
    print("=" * 60)
    print("ROLE-BASED ACCESS CONTROL VERIFICATION")
    print("=" * 60)
    
    # Doctor permissions
    print("\n🩺 DOCTOR PERMISSIONS:")
    print(f"  ✓ View Patients: {check_permission('Doctor', 'patients', 'read')}")
    print(f"  ✓ Add Patients: {check_permission('Doctor', 'patients', 'write')}")
    print(f"  ✓ Update Patients: {check_permission('Doctor', 'patients', 'update')}")
    print(f"  ✓ Delete Patients: {check_permission('Doctor', 'patients', 'delete')}")
    print(f"  ✓ View Reports: {check_permission('Doctor', 'reports', 'read')}")
    print(f"  ✓ Create Reports: {check_permission('Doctor', 'reports', 'write')}")
    print(f"  ✓ View Prescriptions: {check_permission('Doctor', 'prescriptions', 'read')}")
    print(f"  ✓ ADD PRESCRIPTIONS: {check_permission('Doctor', 'prescriptions', 'write')}")
    
    # Nurse permissions
    print("\n👩‍⚕️ NURSE PERMISSIONS:")
    print(f"  ✓ View Patients: {check_permission('Nurse', 'patients', 'read')}")
    print(f"  ✗ Add Patients: {check_permission('Nurse', 'patients', 'write')}")
    print(f"  ✗ Update Patients: {check_permission('Nurse', 'patients', 'update')}")
    print(f"  ✗ Delete Patients: {check_permission('Nurse', 'patients', 'delete')}")
    print(f"  ✓ View Reports: {check_permission('Nurse', 'reports', 'read')}")
    print(f"  ✗ Create Reports: {check_permission('Nurse', 'reports', 'write')}")
    print(f"  ✗ View Prescriptions: {check_permission('Nurse', 'prescriptions', 'read')}")
    print(f"  ✗ ADD PRESCRIPTIONS: {check_permission('Nurse', 'prescriptions', 'write')}")
    
    # Pharmacist permissions
    print("\n💊 PHARMACIST PERMISSIONS:")
    print(f"  ✗ View Patients: {check_permission('Pharmacist', 'patients', 'read')}")
    print(f"  ✗ Add Patients: {check_permission('Pharmacist', 'patients', 'write')}")
    print(f"  ✗ Update Patients: {check_permission('Pharmacist', 'patients', 'update')}")
    print(f"  ✗ Delete Patients: {check_permission('Pharmacist', 'patients', 'delete')}")
    print(f"  ✗ View Reports: {check_permission('Pharmacist', 'reports', 'read')}")
    print(f"  ✗ Create Reports: {check_permission('Pharmacist', 'reports', 'write')}")
    print(f"  ✓ View Prescriptions: {check_permission('Pharmacist', 'prescriptions', 'read')}")
    print(f"  ✗ Add Prescriptions: {check_permission('Pharmacist', 'prescriptions', 'write')}")
    
    print("\n" + "=" * 60)
    print("REQUIREMENTS VERIFICATION")
    print("=" * 60)
    
    # Verify requirements
    req1 = check_permission('Doctor', 'prescriptions', 'write')
    req2_patients = check_permission('Nurse', 'patients', 'read')
    req2_reports = check_permission('Nurse', 'reports', 'read')
    req2_no_prescriptions = not check_permission('Nurse', 'prescriptions', 'write')
    req3_view_prescriptions = check_permission('Pharmacist', 'prescriptions', 'read')
    req3_no_patients = not check_permission('Pharmacist', 'patients', 'read')
    req3_no_reports = not check_permission('Pharmacist', 'reports', 'read')
    
    print(f"\n✅ Req #1 - Doctor can ADD prescriptions: {req1}")
    print(f"✅ Req #2 - Nurse can view patients: {req2_patients}")
    print(f"✅ Req #2 - Nurse can view reports: {req2_reports}")
    print(f"✅ Req #2 - Nurse CANNOT add prescriptions: {req2_no_prescriptions}")
    print(f"✅ Req #3 - Pharmacist can view prescriptions: {req3_view_prescriptions}")
    print(f"✅ Req #3 - Pharmacist CANNOT view patients: {req3_no_patients}")
    print(f"✅ Req #3 - Pharmacist CANNOT view reports: {req3_no_reports}")
    
    all_passed = all([
        req1, req2_patients, req2_reports, req2_no_prescriptions,
        req3_view_prescriptions, req3_no_patients, req3_no_reports
    ])
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL REQUIREMENTS ARE ALREADY CORRECTLY IMPLEMENTED!")
    else:
        print("❌ SOME REQUIREMENTS NEED FIXES")
    print("=" * 60)
    
    # Display raw permissions
    print("\n" + "=" * 60)
    print("RAW PERMISSION CONFIGURATION")
    print("=" * 60)
    for role, perms in ROLE_PERMISSIONS.items():
        print(f"\n{role}:")
        for resource, actions in perms.items():
            print(f"  - {resource}: {actions}")

if __name__ == "__main__":
    verify_permissions()
