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

                "EmployId": employee.EmployId,

                "Employname": employee.Employname,

                "Address": employee.Address,

                "Employrole": employee.Employrole,

                "Designation": employee.Designation,

                "Experince": employee.Experince,

                "Salary": employee.Salary,
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
        # Employee delete hoga.
        #
        # Lekin:
        # Employ_Att delete nahi hoga.
        # Employ_Salary delete nahi hoga.
        #
        # Isliye salary ka last record safe rahega.
        # =================================================

        employee.delete()

        return JsonResponse({

            "success": True,

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

        new_salary = request.POST.get(
            "Salary",
            ""
        )

        # =================================================
        # UPDATE EMPLOYEE DATA
        # =================================================

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
        # UPDATE SALARY RECORD
        #
        # Employee abhi Employ List me hai.
        #
        # Isliye Employ List me salary change karne par
        # Salary page par bhi current salary dikhegi.
        #
        # =================================================

        Employ_Salary.objects.filter(

            EmployId=employee.EmployId

        ).update(

            Employname=new_name,

            MonthlySalary=new_salary
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
        # CONVERT DATE
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
                        "Invalid date format."
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
        # CHECK SALARY RECORD
        # =================================================

        salary_record = Employ_Salary.objects.filter(

            EmployId=employee.EmployId,

            Month=month,

            Year=year

        ).first()

        # =================================================
        # CREATE SALARY RECORD
        #
        # Salary record sirf attendance add hone par
        # create hoga.
        # =================================================

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

        else:

            # =================================================
            # Employee abhi active hai.
            #
            # Isliye current salary use hogi.
            # =================================================

            salary_record.Employname = (
                employee.Employname
            )

            salary_record.MonthlySalary = (
                employee.Salary
            )

            salary_record.save()

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

        # =================================================
        # SAVE DATA BEFORE DELETE
        # =================================================

        employee_id = attendance.EmployId

        month = attendance.Date.month

        year = attendance.Date.year

        # =================================================
        # DELETE ATTENDANCE
        # =================================================

        attendance.delete()

        # =================================================
        # CHECK REMAINING ATTENDANCE
        # =================================================

        remaining_attendance = Employ_Att.objects.filter(

            EmployId=employee_id,

            Date__month=month,

            Date__year=year

        ).exists()

        # =================================================
        # LAST ATTENDANCE DELETE
        #
        # Agar is month ki ek bhi attendance nahi bachi,
        # to salary record delete hoga.
        #
        # =================================================

        if not remaining_attendance:

            Employ_Salary.objects.filter(

                EmployId=employee_id,

                Month=month,

                Year=year

            ).delete()

        return JsonResponse({

            "success":
                True,

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

        new_date_string = request.POST.get(
            "Date"
        )

        new_status = request.POST.get(
            "Status"
        )

        # =================================================
        # CONVERT DATE
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
                        "Invalid date format."
                },
                status=400
            )

        # =================================================
        # DUPLICATE CHECK
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
        # CHECK EMPLOYEE
        # =================================================

        employee = Employ_Data.objects.filter(

            EmployId=attendance.EmployId

        ).first()

        if employee:

            new_month = new_date.month

            new_year = new_date.year

            # =============================================
            # NEW MONTH SALARY RECORD
            # =============================================

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

            else:

                salary_record.Employname = (
                    employee.Employname
                )

                salary_record.MonthlySalary = (
                    employee.Salary
                )

                salary_record.save()

            # =============================================
            # CHECK OLD MONTH
            # =============================================

            old_month_remaining = Employ_Att.objects.filter(

                EmployId=employee.EmployId,

                Date__month=old_month,

                Date__year=old_year

            ).exists()

            # =============================================
            # OLD MONTH EMPTY
            # =============================================

            if not old_month_remaining:

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
    # =====================================================

    salary_records = Employ_Salary.objects.all().order_by(

        "EmployId",

        "Year",

        "Month"
    )

    salary_data = []

    # =====================================================
    # LOOP SALARY
    # =====================================================

    for salary_record in salary_records:

        # =================================================
        # CHECK EMPLOYEE
        # =================================================

        employee = Employ_Data.objects.filter(

            EmployId=salary_record.EmployId

        ).first()

        # =================================================
        # EMPLOYEE EXISTS
        #
        # Current salary use karo.
        # =================================================

        if employee:

            display_name = employee.Employname

            monthly_salary_string = employee.Salary

            # Current salary ko saved salary record me
            # bhi update rakho.

            if (
                str(salary_record.MonthlySalary)
                != str(employee.Salary)
                or
                salary_record.Employname
                != employee.Employname
            ):

                salary_record.MonthlySalary = (
                    employee.Salary
                )

                salary_record.Employname = (
                    employee.Employname
                )

                salary_record.save()

        # =================================================
        # EMPLOYEE DELETE HO CHUKA HAI
        #
        # Ab salary record ki last salary use hogi.
        # =================================================

        else:

            display_name = (
                salary_record.Employname
            )

            monthly_salary_string = (
                salary_record.MonthlySalary
            )

        # =================================================
        # PRESENT COUNT
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
        # HALF DAY COUNT
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
        # ABSENT COUNT
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
        # CONVERT SALARY
        # =================================================

        try:

            monthly_salary = Decimal(
                str(monthly_salary_string)
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
        # SALARY DATA
        # =================================================

        salary_data.append({

            "id":
                salary_record.id,

            "EmployId":
                salary_record.EmployId,

            "Employname":
                display_name,

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