
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from curd_app.models import Employ_Data, Employ_Att


# =========================================================
# EMPLOYEE LIST + ADD EMPLOYEE
# =========================================================

@csrf_exempt
def Employ_list(request):

    if request.method == "GET":

        employees = Employ_Data.objects.all()

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

        return JsonResponse(data, safe=False)


    # -----------------------------------------------------
    # ADD EMPLOYEE
    # -----------------------------------------------------

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
            "message": "Employee added successfully",
            "EmployId": employee.EmployId,
        })


    # -----------------------------------------------------
    # INVALID METHOD
    # -----------------------------------------------------

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

        employee.delete()

        return JsonResponse({
            "success": True,
            "message": "Employee deleted successfully"
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


    # -----------------------------------------------------
    # GET EMPLOYEE
    # -----------------------------------------------------

    if request.method == "GET":

        return JsonResponse({

            "EmployId": employee.EmployId,

            "Employname": employee.Employname,

            "Address": employee.Address,

            "Employrole": employee.Employrole,

            "Designation": employee.Designation,

            "Experince": employee.Experince,

            "Salary": employee.Salary,
        })


    # -----------------------------------------------------
    # UPDATE EMPLOYEE
    # -----------------------------------------------------

    if request.method == "POST":

        employee.Employname = request.POST.get(
            "Employname",
            ""
        )

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

        return JsonResponse({
            "success": True,
            "message": "Employee updated successfully"
        })


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

    # -----------------------------------------------------
    # GET ATTENDANCE
    # -----------------------------------------------------

    if request.method == "GET":

        attendance = Employ_Att.objects.all()

        data = []

        for item in attendance:

            data.append({

                "id": item.id,

                "EmployId": item.EmployId,

                "Employname": item.Employname,

                "Date": str(item.Date),

                "Status": item.Status,
            })

        return JsonResponse(
            data,
            safe=False
        )


    # -----------------------------------------------------
    # ADD ATTENDANCE
    # -----------------------------------------------------

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


        # -------------------------------------------------
        # CHECK EMPLOYEE
        # -------------------------------------------------

        try:

            employee = Employ_Data.objects.get(
                EmployId=employ_id
            )

        except Employ_Data.DoesNotExist:

            return JsonResponse(
                {
                    "success": False,
                    "error": "Employee ID not found."
                },
                status=404
            )


        # -------------------------------------------------
        # CHECK DUPLICATE ATTENDANCE
        # -------------------------------------------------

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


        # -------------------------------------------------
        # CREATE ATTENDANCE
        # -------------------------------------------------

        attendance = Employ_Att.objects.create(

            EmployId=employee.EmployId,

            Employname=employee.Employname,

            Date=date,

            Status=status
        )


        return JsonResponse({
            "success": True,
            "message": "Attendance added successfully",
            "id": attendance.id
        })


    # -----------------------------------------------------
    # INVALID METHOD
    # -----------------------------------------------------

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

        attendance.delete()

        return JsonResponse({
            "success": True,
            "message": "Attendance deleted successfully"
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


    # -----------------------------------------------------
    # GET ATTENDANCE
    # -----------------------------------------------------

    if request.method == "GET":

        return JsonResponse({

            "id": attendance.id,

            "EmployId": attendance.EmployId,

            "Employname": attendance.Employname,

            "Date": str(attendance.Date),

            "Status": attendance.Status,
        })


    # -----------------------------------------------------
    # UPDATE ATTENDANCE
    # -----------------------------------------------------

    if request.method == "POST":

        attendance.Date = request.POST.get(
            "Date"
        )

        attendance.Status = request.POST.get(
            "Status"
        )

        attendance.save()

        return JsonResponse({
            "success": True,
            "message": "Attendance updated successfully"
        })


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

    # -----------------------------------------------------
    # ONLY GET ALLOWED
    # -----------------------------------------------------

    if request.method != "GET":

        return JsonResponse(
            {
                "success": False,
                "error": "Method not allowed"
            },
            status=405
        )


    employees = Employ_Data.objects.all()

    salary_data = []


    # -----------------------------------------------------
    # CALCULATE SALARY FOR EVERY EMPLOYEE
    # -----------------------------------------------------

    for employee in employees:


        # -------------------------------------------------
        # PRESENT COUNT
        # -------------------------------------------------

        present = Employ_Att.objects.filter(

            EmployId=employee.EmployId,

            Status="Present"

        ).count()


        # -------------------------------------------------
        # HALF DAY COUNT
        # -------------------------------------------------

        half_day = Employ_Att.objects.filter(

            EmployId=employee.EmployId,

            Status="Half Day"

        ).count()


        # -------------------------------------------------
        # ABSENT COUNT
        # -------------------------------------------------

        absent = Employ_Att.objects.filter(

            EmployId=employee.EmployId,

            Status="Absent"

        ).count()


        # -------------------------------------------------
        # MONTHLY SALARY
        # -------------------------------------------------

        try:

            monthly_salary = float(
                employee.Salary
            )

        except (
            ValueError,
            TypeError
        ):

            monthly_salary = 0


        # -------------------------------------------------
        # PER DAY SALARY
        # -------------------------------------------------

        per_day_salary = (
            monthly_salary / 31
        )


        # -------------------------------------------------
        # TOTAL SALARY
        # -------------------------------------------------

        total_salary = (

            present * per_day_salary

        ) + (

            half_day
            * 0.5
            * per_day_salary

        )


        # -------------------------------------------------
        # ADD TO RESPONSE
        # -------------------------------------------------

        salary_data.append({

            "EmployId":
                employee.EmployId,

            "Employname":
                employee.Employname,

            "Salary":
                monthly_salary,

            "Present":
                present,

            "HalfDay":
                half_day,

            "Absent":
                absent,

            "TotalSalary":
                round(
                    total_salary,
                    2
                ),
        })


    # -----------------------------------------------------
    # RETURN JSON
    # -----------------------------------------------------

    return JsonResponse(
        salary_data,
        safe=False
    )
