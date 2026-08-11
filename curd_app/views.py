from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from curd_app.models import (
    Employ_Data,
    Employ_Att,
    Employ_Salary
)

from decimal import Decimal, InvalidOperation
from datetime import datetime


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

            "success":
                True,

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
        # Employee delete hone par salary delete nahi hogi.
        #
        # Salary ka record attendance ke basis par control
        # hoga.
        # =================================================

        employee.delete()

        return JsonResponse({

            "success":
                True,

            "message":
                "Employee deleted successfully"
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
        # UPDATE ATTENDANCE NAME
        # =================================================

        Employ_Att.objects.filter(

            EmployId=employee.EmployId

        ).update(

            Employname=new_name
        )

        # =================================================
        # UPDATE EXISTING SALARY NAME
        # =================================================

        Employ_Salary.objects.filter(

            EmployId=employee.EmployId

        ).update(

            Employname=new_name
        )

        return JsonResponse({

            "success":
                True,

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
        # CHECK DATE
        # =================================================

        try:

            attendance_date = datetime.strptime(
                date,
                "%Y-%m-%d"
            ).date()

        except (
            ValueError,
            TypeError
        ):

            return JsonResponse(

                {
                    "success": False,

                    "error":
                        "Invalid date format. "
                        "Use YYYY-MM-DD."
                },

                status=400
            )

        # =================================================
        # CHECK DUPLICATE ATTENDANCE
        # =================================================

        existing_attendance = Employ_Att.objects.filter(

            EmployId=employee.EmployId,

            Date=attendance_date

        ).first()

        if existing_attendance:

            return JsonResponse(

                {
                    "success": False,

                    "error":
                        "This employee attendance is "
                        "already marked for this date."
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
                attendance_date,

            Status=
                status
        )

        # =================================================
        # MONTH + YEAR
        # =================================================

        month = attendance_date.month

        year = attendance_date.year

        # =================================================
        # MONTHLY SALARY
        # =================================================

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

        # =================================================
        # CREATE SALARY RECORD
        #
        # Same employee + same month/year ka sirf
        # ek salary record rahega.
        # =================================================

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
                    str(monthly_salary),

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

        # =================================================
        # GET ATTENDANCE
        # =================================================

        attendance = get_object_or_404(
            Employ_Att,
            id=id
        )

        # =================================================
        # SAVE EMPLOYEE + MONTH + YEAR
        # BEFORE DELETE
        # =================================================

        employee_id = attendance.EmployId

        attendance_month = attendance.Date.month

        attendance_year = attendance.Date.year

        # =================================================
        # DELETE ONLY THIS ATTENDANCE
        # =================================================

        attendance.delete()

        # =================================================
        # CHECK REMAINING ATTENDANCE
        #
        # Same employee + same month + same year
        # me koi attendance bachi hai?
        # =================================================

        remaining_attendance = Employ_Att.objects.filter(

            EmployId=employee_id,

            Date__month=attendance_month,

            Date__year=attendance_year

        ).exists()

        # =================================================
        # AGAR KOI ATTENDANCE NAHI BACCHI
        #
        # TO US MONTH KA SALARY RECORD DELETE
        # =================================================

        if not remaining_attendance:

            Employ_Salary.objects.filter(

                EmployId=employee_id,

                Month=attendance_month,

                Year=attendance_year

            ).delete()

        # =================================================
        # RESPONSE
        # =================================================

        return JsonResponse({

            "success":
                True,

            "message":
                "Attendance deleted successfully"
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

        new_date_string = request.POST.get(
            "Date"
        )

        new_status = request.POST.get(
            "Status"
        )

        # =================================================
        # CHECK NEW DATE
        # =================================================

        try:

            new_date = datetime.strptime(
                new_date_string,
                "%Y-%m-%d"
            ).date()

        except (
            ValueError,
            TypeError
        ):

            return JsonResponse(

                {
                    "success": False,

                    "error":
                        "Invalid date format. "
                        "Use YYYY-MM-DD."
                },

                status=400
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
                        "This employee attendance is "
                        "already marked for this date."
                },

                status=400
            )

        # =================================================
        # UPDATE ATTENDANCE
        # =================================================

        attendance.Date = new_date

        attendance.Status = new_status

        attendance.save()

        # =================================================
        # GET EMPLOYEE
        # =================================================

        employee = Employ_Data.objects.filter(

            EmployId=attendance.EmployId

        ).first()

        if employee:

            # =============================================
            # NEW MONTH/YEAR
            # =============================================

            new_month = new_date.month

            new_year = new_date.year

            # =============================================
            # MONTHLY SALARY
            # =============================================

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

            # =============================================
            # CREATE NEW MONTH SALARY IF NEEDED
            # =============================================

            Employ_Salary.objects.get_or_create(

                EmployId=
                    employee.EmployId,

                Month=
                    new_month,

                Year=
                    new_year,

                defaults={

                    "Employname":
                        employee.Employname,

                    "MonthlySalary":
                        str(monthly_salary)
                }
            )

            # =============================================
            # OLD MONTH ME ATTENDANCE BACHI HAI?
            # =============================================

            old_month_attendance = Employ_Att.objects.filter(

                EmployId=
                    employee.EmployId,

                Date__month=
                    old_month,

                Date__year=
                    old_year

            ).exists()

            # =============================================
            # AGAR OLD MONTH EMPTY HO GAYA
            # TO OLD MONTH SALARY DELETE
            # =============================================

            if not old_month_attendance:

                Employ_Salary.objects.filter(

                    EmployId=
                        employee.EmployId,

                    Month=
                        old_month,

                    Year=
                        old_year

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
    # ONLY GET
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
    # Salary page Employ_Data se nahi,
    # Employ_Salary se data lega.
    #
    # Isliye Employee List se employee delete hone par
    # salary record automatically disappear nahi hoga.
    # =====================================================

    salary_records = Employ_Salary.objects.all().order_by(

        "EmployId",

        "Year",

        "Month"
    )

    salary_data = []

    # =====================================================
    # CALCULATE EACH MONTH SALARY
    # =====================================================

    for salary_record in salary_records:

        # =================================================
        # PRESENT
        # =================================================

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

        # =================================================
        # HALF DAY
        # =================================================

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

        # =================================================
        # ABSENT
        # =================================================

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

                str(
                    salary_record.MonthlySalary
                )

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

            monthly_salary /
            Decimal("31")

        )

        # =================================================
        # TOTAL SALARY
        # =================================================

        total_salary = (

            Decimal(present) *
            per_day_salary

        ) + (

            Decimal(half_day) *
            Decimal("0.5") *
            per_day_salary

        )

        # =================================================
        # SALARY DATA
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
    # RETURN
    # =====================================================

    return JsonResponse(

        salary_data,

        safe=False
    )