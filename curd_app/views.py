from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from curd_app.models import (
    Employ_Data,
    Employ_Att,
    Employ_Salary
)

from decimal import Decimal, InvalidOperation


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

        # =================================================
        # IMPORTANT
        #
        # Yahan Employ_Salary ko delete nahi karna.
        #
        # Isliye employee delete hone ke baad bhi
        # salary page ka record safe rahega.
        # =================================================

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

        employee.Salary = request.POST.get(
            "Salary",
            ""
        )

        employee.save()

        # =================================================
        # UPDATE EXISTING ATTENDANCE NAME
        # =================================================

        Employ_Att.objects.filter(
            EmployId=employee.EmployId
        ).update(
            Employname=new_name
        )

        # =================================================
        # IMPORTANT
        #
        # Existing salary records ka naam bhi update hoga.
        # MonthlySalary change nahi kar rahe yahan.
        # =================================================

        Employ_Salary.objects.filter(
            EmployId=employee.EmployId
        ).update(
            Employname=new_name
        )

        return JsonResponse({

            "success": True,

            "message":
                "Employee, attendance and salary name updated successfully"
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
        # CREATE / SAVE MONTHLY SALARY
        #
        # Attendance add karte waqt salary record ensure
        # hoga.
        #
        # Agar same employee + same month ka salary record
        # already hai to duplicate nahi banega.
        # =================================================

        try:

            attendance_date = attendance.Date

            month = attendance_date.month

            year = attendance_date.year

        except Exception:

            today = timezone.now().date()

            month = today.month

            year = today.year

        # =================================================
        # CHECK EXISTING SALARY
        # =================================================

        salary_record = Employ_Salary.objects.filter(

            EmployId=employee.EmployId,

            Month=month,

            Year=year

        ).first()

        # =================================================
        # SALARY RECORD DOES NOT EXIST
        # =================================================

        if not salary_record:

            try:

                monthly_salary = Decimal(
                    str(employee.Salary)
                )

            except (
                InvalidOperation,
                ValueError,
                TypeError
            ):

                monthly_salary = Decimal("0")

            Employ_Salary.objects.create(

                EmployId=
                    employee.EmployId,

                Employname=
                    employee.Employname,

                MonthlySalary=
                    monthly_salary,

                Month=
                    month,

                Year=
                    year
            )

        # =================================================
        # RESPONSE
        # =================================================

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

        # =================================================
        # DELETE ONLY THIS ATTENDANCE
        #
        # Salary record delete nahi hoga.
        # =================================================

        attendance.delete()

        # =================================================
        # IMPORTANT
        #
        # Agar employee ki koi bhi attendance remaining hai
        # to salary record definitely rahega.
        #
        # Agar employee ki saari attendance delete ho gayi,
        # tab bhi Monthly Salary record preserve rahega
        # according to your latest requirement.
        # =================================================

        return JsonResponse({

            "success": True,

            "message":
                "Attendance deleted successfully. Salary record preserved."
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

        old_date = attendance.Date

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

        attendance.Date = new_date

        attendance.Status = new_status

        attendance.save()

        # =================================================
        # SALARY FOR NEW MONTH
        #
        # Agar attendance edit karke kisi naye month me gayi
        # aur us month ka salary record nahi hai,
        # to create kar denge.
        # =================================================

        employee = Employ_Data.objects.filter(
            EmployId=attendance.EmployId
        ).first()

        if employee:

            try:

                monthly_salary = Decimal(
                    str(employee.Salary)
                )

            except (
                InvalidOperation,
                ValueError,
                TypeError
            ):

                monthly_salary = Decimal("0")

            month = attendance.Date.month

            year = attendance.Date.year

            Employ_Salary.objects.get_or_create(

                EmployId=
                    employee.EmployId,

                Month=
                    month,

                Year=
                    year,

                defaults={

                    "Employname":
                        employee.Employname,

                    "MonthlySalary":
                        monthly_salary
                }
            )

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
    # GET SALARY RECORDS
    #
    # IMPORTANT:
    # Employ_Data se salary nahi nikalenge.
    #
    # Employ_Salary se nikalenge.
    #
    # Isliye employee delete hone ke baad bhi salary
    # page par record rahega.
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
        # PRESENT COUNT
        #
        # Sirf same employee + same month + same year
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
        # HALF DAY COUNT
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
        # ABSENT COUNT
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
        # =================================================

        try:

            monthly_salary = Decimal(
                str(salary_record.MonthlySalary)
            )

        except (
            InvalidOperation,
            ValueError,
            TypeError
        ):

            monthly_salary = Decimal("0")

        # =================================================
        # PER DAY SALARY
        # =================================================

        per_day_salary = (
            monthly_salary / Decimal("31")
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
        # =================================================

        salary_data.append({

            "id":
                salary_record.id,

            "EmployId":
                salary_record.EmployId,

            "Employname":
                salary_record.Employname,

            "Salary":
                float(monthly_salary),

            "MonthlySalary":
                float(monthly_salary),

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
                float(
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