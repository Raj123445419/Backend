from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


from curd_app.models import (
    Employ_Data,
    Employ_Att,
    Employ_Salary
)

from decimal import Decimal, InvalidOperation


# =========================================================
# SAFE SALARY CONVERSION
# =========================================================

def safe_salary(value):

    try:

        value = str(value).strip()

        if not value:
            return Decimal("0")

        return Decimal(value)

    except (
        InvalidOperation,
        ValueError,
        TypeError
    ):

        return Decimal("0")


# =========================================================
# EMPLOYEE LIST + ADD EMPLOYEE
# =========================================================

@csrf_exempt
def Employ_list(request):

    # =====================================================
    # GET EMPLOYEE LIST
    # =====================================================

    if request.method == "GET":

        employees = Employ_Data.objects.all().order_by(
            "EmployId"
        )

        data = []

        for employee in employees:

            data.append({

                "EmployId":
                    employee.EmployId,

                "Employname":
                    employee.Employname,

                "Address":
                    employee.Address,

                "Employrole":
                    employee.Employrole,

                "Designation":
                    employee.Designation,

                "Experince":
                    employee.Experince,

                "Salary":
                    employee.Salary,
            })

        return JsonResponse(
            data,
            safe=False
        )

    # =====================================================
    # ADD EMPLOYEE
    # =====================================================

    if request.method == "POST":

        employee = Employ_Data.objects.create(

            Employname=request.POST.get(
                "Employname",
                ""
            ),

            Address=request.POST.get(
                "Address",
                ""
            ),

            Employrole=request.POST.get(
                "Employrole",
                ""
            ),

            Designation=request.POST.get(
                "Designation",
                ""
            ),

            Experince=request.POST.get(
                "Experince",
                ""
            ),

            Salary=request.POST.get(
                "Salary",
                ""
            ),
        )

        return JsonResponse({

            "success": True,

            "message":
                "Employee added successfully",

            "EmployId":
                employee.EmployId,
        })

    # =====================================================
    # INVALID METHOD
    # =====================================================

    return JsonResponse(
        {
            "success": False,
            "error": "Method not allowed"
        },
        status=405
    )


# =========================================================
# DELETE EMPLOYEE
# =========================================================

@csrf_exempt
def Delete(request, id):

    if request.method in ["DELETE", "POST"]:

        employee = get_object_or_404(
            Employ_Data,
            EmployId=id
        )

        # -------------------------------------------------
        # Employee delete hone par salary record delete
        # nahi hoga.
        # -------------------------------------------------

        employee.delete()

        return JsonResponse({

            "success": True,

            "message":
                "Employee deleted successfully. Salary record preserved."
        })

    return JsonResponse(
        {
            "success": False,
            "error": "Method not allowed"
        },
        status=405
    )


# =========================================================
# EDIT EMPLOYEE
# =========================================================

@csrf_exempt
def Edite(request, id):

    employee = get_object_or_404(
        Employ_Data,
        EmployId=id
    )

    # =====================================================
    # GET EMPLOYEE
    # =====================================================

    if request.method == "GET":

        return JsonResponse({

            "EmployId":
                employee.EmployId,

            "Employname":
                employee.Employname,

            "Address":
                employee.Address,

            "Employrole":
                employee.Employrole,

            "Designation":
                employee.Designation,

            "Experince":
                employee.Experince,

            "Salary":
                employee.Salary,
        })

    # =====================================================
    # UPDATE EMPLOYEE
    # =====================================================

    if request.method == "POST":

        new_name = request.POST.get(
            "Employname",
            ""
        )

        new_salary = request.POST.get(
            "Salary",
            ""
        )

        employee.Employname = new_name

        employee.Address = request.POST.get(
            "Address",
            ""
        )

        employee.Employrole = request.POST.get(
            "Employrole",
            ""
        )

        employee.Designation = request.POST.get(
            "Designation",
            ""
        )

        employee.Experince = request.POST.get(
            "Experince",
            ""
        )

        # -------------------------------------------------
        # Salary ko TextField me hi save kar rahe hain.
        # Isliye koi fixed numeric limit nahi.
        # -------------------------------------------------

        employee.Salary = new_salary

        employee.save()

        # =================================================
        # UPDATE ATTENDANCE NAME
        # =================================================

        Employ_Att.objects.filter(
            EmployId=employee.EmployId
        ).update(
            Employname=new_name
        )

        # =================================================
        # IMPORTANT
        #
        # Existing salary record ki MonthlySalary ko
        # yahan change nahi karenge.
        #
        # Kyunki old month ka salary record preserve
        # rehna chahiye.
        # =================================================

        Employ_Salary.objects.filter(
            EmployId=employee.EmployId
        ).update(
            Employname=new_name
        )

        return JsonResponse({

            "success": True,

            "message":
                "Employee updated successfully"
        })

    # =====================================================
    # INVALID METHOD
    # =====================================================

    return JsonResponse(
        {
            "success": False,
            "error": "Method not allowed"
        },
        status=405
    )


# =========================================================
# ATTENDANCE LIST + ADD ATTENDANCE
# =========================================================

@csrf_exempt
def Employ_attendance(request):

    # =====================================================
    # GET ATTENDANCE
    # =====================================================

    if request.method == "GET":

        attendance = Employ_Att.objects.all().order_by(
            "id"
        )

        data = []

        for item in attendance:

            data.append({

                "id":
                    item.id,

                "EmployId":
                    item.EmployId,

                "Employname":
                    item.Employname,

                "Date":
                    str(item.Date),

                "Status":
                    item.Status,
            })

        return JsonResponse(
            data,
            safe=False
        )

    # =====================================================
    # ADD ATTENDANCE
    # =====================================================

    if request.method == "POST":

        employ_id = request.POST.get(
            "EmployId"
        )

        date = request.POST.get(
            "Date"
        )

        status = request.POST.get(
            "Status"
        )

        # =================================================
        # CHECK EMPLOYEE
        # =================================================

        try:

            employee = Employ_Data.objects.get(
                EmployId=employ_id
            )

        except Employ_Data.DoesNotExist:

            return JsonResponse(
                {
                    "success": False,
                    "error":
                        "Employee ID not found."
                },
                status=404
            )

        # =================================================
        # CHECK DUPLICATE ATTENDANCE
        # =================================================

        existing_attendance = Employ_Att.objects.filter(

            EmployId=employee.EmployId,

            Date=date

        ).first()

        if existing_attendance:

            return JsonResponse(
                {
                    "success": False,

                    "error":
                        "This employee attendance is already "
                        "marked for this date."
                },
                status=400
            )

        # =================================================
        # CREATE ATTENDANCE
        # =================================================

        attendance = Employ_Att.objects.create(

            EmployId=
                employee.EmployId,

            Employname=
                employee.Employname,

            Date=
                date,

            Status=
                status
        )

        # =================================================
        # CREATE MONTHLY SALARY RECORD
        #
        # Pehli attendance par current attendance ke
        # month/year ka salary record create hoga.
        #
        # Same month me dusri attendance par duplicate
        # salary record nahi banega.
        # =================================================

        month = attendance.Date.month

        year = attendance.Date.year

        salary_record = Employ_Salary.objects.filter(

            EmployId=employee.EmployId,

            Month=month,

            Year=year

        ).first()

        if not salary_record:

            Employ_Salary.objects.create(

                EmployId=
                    employee.EmployId,

                Employname=
                    employee.Employname,

                MonthlySalary=
                    employee.Salary,

                Month=
                    month,

                Year=
                    year
            )

        return JsonResponse({

            "success":
                True,

            "message":
                "Attendance added successfully",

            "id":
                attendance.id
        })

    # =====================================================
    # INVALID METHOD
    # =====================================================

    return JsonResponse(
        {
            "success": False,
            "error": "Method not allowed"
        },
        status=405
    )


# =========================================================
# DELETE ATTENDANCE
# =========================================================

@csrf_exempt
def Delete_attendance(request, id):

    if request.method in ["DELETE", "POST"]:

        attendance = get_object_or_404(
            Employ_Att,
            id=id
        )

        employee_id = attendance.EmployId

        month = attendance.Date.month

        year = attendance.Date.year

        # -------------------------------------------------
        # Attendance delete
        # -------------------------------------------------

        attendance.delete()

        # =================================================
        # CHECK REMAINING ATTENDANCE
        #
        # Agar is employee ki isi month/year me ek bhi
        # attendance nahi bachi, to salary record delete.
        # =================================================

        remaining_attendance = Employ_Att.objects.filter(

            EmployId=employee_id,

            Date__month=month,

            Date__year=year

        ).exists()

        if not remaining_attendance:

            Employ_Salary.objects.filter(

                EmployId=employee_id,

                Month=month,

                Year=year

            ).delete()

        return JsonResponse({

            "success": True,

            "message":
                "Attendance deleted successfully"
        })

    return JsonResponse(
        {
            "success": False,
            "error": "Method not allowed"
        },
        status=405
    )


# =========================================================
# EDIT ATTENDANCE
# =========================================================

@csrf_exempt
def Edite_attendance(request, id):

    attendance = get_object_or_404(
        Employ_Att,
        id=id
    )

    # =====================================================
    # GET ATTENDANCE
    # =====================================================

    if request.method == "GET":

        return JsonResponse({

            "id":
                attendance.id,

            "EmployId":
                attendance.EmployId,

            "Employname":
                attendance.Employname,

            "Date":
                str(attendance.Date),

            "Status":
                attendance.Status,
        })

    # =====================================================
    # UPDATE ATTENDANCE
    # =====================================================

    if request.method == "POST":

        old_month = attendance.Date.month

        old_year = attendance.Date.year

        new_date = request.POST.get(
            "Date"
        )

        new_status = request.POST.get(
            "Status"
        )

        # =================================================
        # CHECK DUPLICATE DATE
        # =================================================

        duplicate = Employ_Att.objects.filter(

            EmployId=attendance.EmployId,

            Date=new_date

        ).exclude(
            id=attendance.id
        ).exists()

        if duplicate:

            return JsonResponse(
                {
                    "success": False,

                    "error":
                        "This employee attendance is already "
                        "marked for this date."
                },
                status=400
            )

        # =================================================
        # SAVE ATTENDANCE
        # =================================================

        attendance.Date = new_date

        attendance.Status = new_status

        attendance.save()

        # =================================================
        # EMPLOYEE
        # =================================================

        employee = Employ_Data.objects.filter(
            EmployId=attendance.EmployId
        ).first()

        if employee:

            new_month = attendance.Date.month

            new_year = attendance.Date.year

            # ---------------------------------------------
            # Agar new month ka salary record nahi hai
            # to current employee salary se create karo.
            # ---------------------------------------------

            salary_record = Employ_Salary.objects.filter(

                EmployId=employee.EmployId,

                Month=new_month,

                Year=new_year

            ).first()

            if not salary_record:

                Employ_Salary.objects.create(

                    EmployId=
                        employee.EmployId,

                    Employname=
                        employee.Employname,

                    MonthlySalary=
                        employee.Salary,

                    Month=
                        new_month,

                    Year=
                        new_year
                )

            # ---------------------------------------------
            # Old month me attendance nahi bachi to old
            # month salary record delete.
            # ---------------------------------------------

            if (
                old_month != new_month
                or
                old_year != new_year
            ):

                old_attendance_exists = Employ_Att.objects.filter(

                    EmployId=employee.EmployId,

                    Date__month=old_month,

                    Date__year=old_year

                ).exists()

                if not old_attendance_exists:

                    Employ_Salary.objects.filter(

                        EmployId=employee.EmployId,

                        Month=old_month,

                        Year=old_year

                    ).delete()

        return JsonResponse({

            "success":
                True,

            "message":
                "Attendance updated successfully"
        })

    # =====================================================
    # INVALID METHOD
    # =====================================================

    return JsonResponse(
        {
            "success": False,
            "error": "Method not allowed"
        },
        status=405
    )


# =========================================================
# SALARY
# =========================================================

def Employ_Sallery(request):

    # =====================================================
    # ONLY GET ALLOWED
    # =====================================================

    if request.method != "GET":

        return JsonResponse(
            {
                "success": False,
                "error": "Method not allowed"
            },
            status=405
        )

    # =====================================================
    # GET SAVED SALARY RECORDS
    #
    # Salary page Employ_Data se nahi,
    # Employ_Salary se data lega.
    #
    # Isliye employee delete hone ke baad bhi jis month
    # ka salary record hai wo preserve rahega.
    # =====================================================

    salary_records = Employ_Salary.objects.all().order_by(

        "EmployId",

        "Year",

        "Month"
    )

    salary_data = []

    # =====================================================
    # CALCULATE SALARY
    # =====================================================

    for salary_record in salary_records:

        # -------------------------------------------------
        # PRESENT
        # -------------------------------------------------

        present = Employ_Att.objects.filter(

            EmployId=
                salary_record.EmployId,

            Status=
                "Present",

            Date__month=
                salary_record.Month,

            Date__year=
                salary_record.Year

        ).count()

        # -------------------------------------------------
        # HALF DAY
        # -------------------------------------------------

        half_day = Employ_Att.objects.filter(

            EmployId=
                salary_record.EmployId,

            Status=
                "Half Day",

            Date__month=
                salary_record.Month,

            Date__year=
                salary_record.Year

        ).count()

        # -------------------------------------------------
        # ABSENT
        # -------------------------------------------------

        absent = Employ_Att.objects.filter(

            EmployId=
                salary_record.EmployId,

            Status=
                "Absent",

            Date__month=
                salary_record.Month,

            Date__year=
                salary_record.Year

        ).count()

        # =================================================
        # MONTHLY SALARY
        #
        # IMPORTANT:
        # safe_salary use kar rahe hain.
        # =================================================

        monthly_salary = safe_salary(
            salary_record.MonthlySalary
        )

        # =================================================
        # PER DAY SALARY
        # =================================================

        per_day_salary = (
            monthly_salary /
            Decimal("31")
        )

        # =================================================
        # TOTAL SALARY
        # =================================================

        total_salary = (

            Decimal(present)
            *
            per_day_salary

        ) + (

            Decimal(half_day)
            *
            Decimal("0.5")
            *
            per_day_salary

        )

        # =================================================
        # ADD DATA
        #
        # IMPORTANT:
        # float() bilkul nahi use karna.
        #
        # Isse extremely large salary bhi safe rahegi.
        # =================================================

        salary_data.append({

            "id":
                salary_record.id,

            "EmployId":
                salary_record.EmployId,

            "Employname":
                salary_record.Employname,

            "Salary":
                str(monthly_salary),

            "MonthlySalary":
                str(monthly_salary),

            "Month":
                salary_record.Month,

            "Year":
                salary_record.Year,

            "Present":
                present,

            "HalfDay":
                half_day,

            "Absent":
                absent,

            "TotalSalary":
                str(
                    round(
                        total_salary,
                        2
                    )
                ),
        })

    # =====================================================
    # RETURN JSON
    # =====================================================

    return JsonResponse(
        salary_data,
        safe=False
    )










from datetime import datetime

def mark_attendance_via_qr(request):
    employ_id = request.GET.get("EmployId")
    date_str = request.GET.get("Date")
    
    if not employ_id or not date_str:
        return HttpResponse("<h2 style='color:red; text-align:center; margin-top:50px;'>Invalid QR Code Data!</h2>")

    try:
        employee = Employ_Data.objects.get(EmployId=employ_id)
        employ_name = employee.Employname
    except Employ_Data.DoesNotExist:
        return HttpResponse("<h2 style='color:red; text-align:center; margin-top:50px;'>Employee Not Found!</h2>")

    # YAHAN CHANGE KIYA HAI: String date ko proper Date object me badla hai
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return HttpResponse("<h2 style='color:red; text-align:center; margin-top:50px;'>Invalid Date Format!</h2>")

    # Check karein ki kya aaj ki attendance pehle se saved hai
    already_marked = Employ_Att.objects.filter(EmployId=employ_id, Date=date_obj).exists()

    if not already_marked:
        attendance = Employ_Att.objects.create(
            EmployId=employ_id,
            Employname=employ_name,
            Date=date_obj,
            Status="Present"
        )

        # Ab yahan date_obj se safely month aur year mil jayega
        month = date_obj.month
        year = date_obj.year

        salary_record = Employ_Salary.objects.filter(
            EmployId=employee.EmployId,
            Month=month,
            Year=year
        ).first()

        if not salary_record:
            Employ_Salary.objects.create(
                EmployId=employee.EmployId,
                Employname=employee.Employname,
                MonthlySalary=employee.Salary,
                Month=month,
                Year=year
            )

        return HttpResponse(f"<h1 style='color:green; text-align:center; margin-top:100px;'>✅ Attendance Saved Successfully!<br>Employee: {employ_name} (ID: {employ_id})</h1>")
    else:
        return HttpResponse(f"<h1 style='color:orange; text-align:center; margin-top:100px;'>⚠️ Attendance Already Marked for {employ_name}!</h1>")