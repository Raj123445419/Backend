from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from curd_app.models import (
    Employ_Data,
    Employ_Att,
    Employ_Salary
)

from decimal import Decimal, InvalidOperation


# =========================================================
# HELPER FUNCTION
# CREATE MONTHLY SALARY RECORD
# =========================================================

def create_salary_record(
    employee_id,
    employee_name,
    monthly_salary,
    month,
    year
):

    # =====================================================
    # Check existing salary record
    # =====================================================

    salary_record = Employ_Salary.objects.filter(

        EmployId=employee_id,

        Month=month,

        Year=year

    ).first()

    # =====================================================
    # Agar already hai to wahi return karo
    # =====================================================

    if salary_record:

        return salary_record

    # =====================================================
    # Salary ko safely Decimal mein convert karo
    # =====================================================

    try:

        salary_value = Decimal(
            str(monthly_salary)
        )

    except (
        InvalidOperation,
        ValueError,
        TypeError
    ):

        salary_value = Decimal("0")

    # =====================================================
    # CREATE SALARY RECORD
    # =====================================================

    salary_record = Employ_Salary.objects.create(

        EmployId=employee_id,

        Employname=employee_name,

        MonthlySalary=str(
            salary_value
        ),

        Month=month,

        Year=year
    )

    return salary_record


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
                employee.EmployId

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
        # Employee delete hone par:
        #
        # Employ_Salary DELETE NAHI HOGI.
        #
        # Salary history safe rahegi.
        # =================================================

        employee.delete()

        return JsonResponse({

            "success":
                True,

            "message":
                "Employee deleted successfully. Salary records preserved."

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
        # IMPORTANT
        #
        # Existing salary records ka naam update hoga.
        #
        # Lekin MonthlySalary ko change nahi karenge.
        #
        # Kyunki salary record jis month mein bana tha,
        # us month ki salary fixed rehni chahiye.
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
        # CREATE MONTHLY SALARY RECORD
        #
        # FIRST ATTENDANCE OF MONTH:
        #
        # Salary record create hoga.
        #
        # SECOND / THIRD / FOURTH ATTENDANCE:
        #
        # Duplicate salary record nahi banega.
        # =================================================

        create_salary_record(

            employee_id=
                employee.EmployId,

            employee_name=
                employee.Employname,

            monthly_salary=
                employee.Salary,

            month=
                attendance.Date.month,

            year=
                attendance.Date.year

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

        # =================================================
        # IMPORTANT
        #
        # Sirf attendance delete hogi.
        #
        # Salary record DELETE NAHI HOGA.
        #
        # Example:
        #
        # 3 Present
        # DELETE 1
        # = 2 Present
        #
        # Salary record same rahega.
        #
        # Sab attendance delete:
        # = Present 0
        #
        # Lekin Monthly Salary row rahegi.
        # =================================================

        attendance.delete()

        return JsonResponse({

            "success":
                True,

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

        # =================================================
        # IMPORTANT
        #
        # Agar employee abhi Employ_Data mein hai,
        # aur attendance ko kisi naye month mein move
        # kiya gaya hai, to naye month ka salary record
        # create karenge.
        #
        # Purane month ka salary record delete NAHI hoga.
        # =================================================

        if employee:

            create_salary_record(

                employee_id=
                    employee.EmployId,

                employee_name=
                    employee.Employname,

                monthly_salary=
                    employee.Salary,

                month=
                    attendance.Date.month,

                year=
                    attendance.Date.year

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
    # IMPORTANT
    #
    # Ye part purani attendance ke liye hai.
    #
    # Agar attendance already database mein hai
    # lekin salary record nahi bana tha,
    # to salary record automatically create hoga.
    #
    # Isse tumhari purani attendance bhi Salary page
    # par dikhegi.
    # =====================================================

    attendance_list = Employ_Att.objects.all()

    for attendance in attendance_list:

        employee_id = attendance.EmployId

        month = attendance.Date.month

        year = attendance.Date.year

        # =================================================
        # Salary record check
        # =================================================

        salary_exists = Employ_Salary.objects.filter(

            EmployId=employee_id,

            Month=month,

            Year=year

        ).exists()

        # =================================================
        # Missing salary record
        # =================================================

        if not salary_exists:

            employee = Employ_Data.objects.filter(

                EmployId=employee_id

            ).first()

            # ---------------------------------------------
            # Employee abhi Employee List mein hai
            # ---------------------------------------------

            if employee:

                create_salary_record(

                    employee_id=
                        employee.EmployId,

                    employee_name=
                        employee.Employname,

                    monthly_salary=
                        employee.Salary,

                    month=
                        month,

                    year=
                        year

                )

            # ---------------------------------------------
            # Employee delete ho chuka hai
            # ---------------------------------------------

            else:

                # IMPORTANT:
                #
                # Deleted employee ke purane attendance
                # record se salary history create karna hai.
                #
                # Lekin salary amount Employ_Data mein nahi hai.
                #
                # Is case mein agar salary record pehle se nahi
                # tha to 0 create hoga.
                #
                # Existing salary record kabhi delete nahi hoga.

                create_salary_record(

                    employee_id=
                        attendance.EmployId,

                    employee_name=
                        attendance.Employname,

                    monthly_salary=
                        "0",

                    month=
                        month,

                    year=
                        year

                )

    # =====================================================
    # GET ALL SALARY RECORDS
    #
    # Employee delete ho gaya ho tab bhi ye record
    # database mein rahega.
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

        # =================================================
        # PRESENT COUNT
        # =================================================

        present = Employ_Att.objects.filter(

            EmployId=
                salary_record.EmployId,

            Date__month=
                salary_record.Month,

            Date__year=
                salary_record.Year

        ).filter(

            Status__iexact=
                "Present"

        ).count()

        # =================================================
        # HALF DAY COUNT
        # =================================================

        half_day = Employ_Att.objects.filter(

            EmployId=
                salary_record.EmployId,

            Date__month=
                salary_record.Month,

            Date__year=
                salary_record.Year

        ).filter(

            Status__iexact=
                "Half Day"

        ).count()

        # =================================================
        # ABSENT COUNT
        # =================================================

        absent = Employ_Att.objects.filter(

            EmployId=
                salary_record.EmployId,

            Date__month=
                salary_record.Month,

            Date__year=
                salary_record.Year

        ).filter(

            Status__iexact=
                "Absent"

        ).count()

        # =================================================
        # MONTHLY SALARY
        #
        # Ye salary record se aayegi.
        #
        # Employ_Data se nahi.
        #
        # Isliye employee ki current salary change
        # karne par purani month salary change nahi hogi.
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
        #
        # Present = 1 day
        # Half Day = 0.5 day
        # Absent = 0
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
                float(
                    monthly_salary
                ),

            "MonthlySalary":
                float(
                    monthly_salary
                ),

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