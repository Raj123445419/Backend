from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from curd_app.models import Employ_Data, Employ_Att


# =========================================================
# EMPLOYEE LIST + ADD EMPLOYEE
# =========================================================

@csrf_exempt
def Employ_list(request):

    # =====================================================
    # GET EMPLOYEE LIST
    # =====================================================

    if request.method == "GET":

        # EmployId ke according fixed order
        employees = Employ_Data.objects.all().order_by("EmployId")

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
        # Employee delete hone par ATTENDANCE DELETE
        # NAHI hogi.
        #
        # Attendance database me safe rahegi.
        #
        # Isliye Salary bhi safe rahegi.
        # =================================================

        employee.delete()

        return JsonResponse({

            "success":
                True,

            "message":
                "Employee deleted successfully. Attendance records are preserved."
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

        # -------------------------------------------------
        # NEW EMPLOYEE NAME
        # -------------------------------------------------

        new_name = request.POST.get(
            "Employname",
            ""
        )

        # -------------------------------------------------
        # UPDATE EMPLOYEE DATA
        # -------------------------------------------------

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

        # -------------------------------------------------
        # SAVE EMPLOYEE
        # -------------------------------------------------

        employee.save()

        # =================================================
        # IMPORTANT
        #
        # Employee ka name aur salary change hone par
        # existing attendance records me bhi update hoga.
        #
        # Employee delete hone par ye records delete
        # nahi hote.
        # =================================================

        Employ_Att.objects.filter(
            EmployId=employee.EmployId
        ).update(
            Employname=new_name,
            Salary=employee.Salary
        )

        return JsonResponse({

            "success":
                True,

            "message":
                "Employee and attendance records updated successfully"
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

        # Attendance ID ke according fixed order
        attendance = Employ_Att.objects.all().order_by("id")

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

                # Salary bhi frontend ko bhej rahe hain
                "Salary":
                    item.Salary,
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
        #
        # IMPORTANT:
        #
        # Employee ki Salary Attendance ke andar save
        # kar rahe hain.
        #
        # Isse Employee delete hone ke baad bhi Salary
        # calculate ho sakti hai.
        #
        # =================================================

        attendance = Employ_Att.objects.create(

            EmployId=
                employee.EmployId,

            Employname=
                employee.Employname,

            Salary=
                employee.Salary,

            Date=
                date,

            Status=
                status
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

        # =================================================
        # IMPORTANT
        #
        # Sirf ye attendance record delete hoga.
        #
        # Salary manually delete nahi karni hai.
        #
        # Salary API remaining attendance records ko count
        # karke automatically salary calculate karegi.
        #
        # Agar ye employee ki LAST attendance hai,
        # to Employ_Att me us employee ka koi record
        # nahi bachega.
        #
        # Is case me Salary API us employee ko return
        # nahi karegi.
        # =================================================

        employ_id = attendance.EmployId

        attendance.delete()

        # =================================================
        # CHECK REMAINING ATTENDANCE
        # =================================================

        remaining_attendance = Employ_Att.objects.filter(
            EmployId=employ_id
        ).exists()

        return JsonResponse({

            "success":
                True,

            "message":
                "Attendance deleted successfully",

            "EmployId":
                employ_id,

            "remaining_attendance":
                remaining_attendance
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

            "Salary":
                attendance.Salary,
        })

    # =====================================================
    # UPDATE ATTENDANCE
    # =====================================================

    if request.method == "POST":

        # -------------------------------------------------
        # DATE
        # -------------------------------------------------

        attendance.Date = request.POST.get(
            "Date"
        )

        # -------------------------------------------------
        # STATUS
        # -------------------------------------------------

        attendance.Status = request.POST.get(
            "Status"
        )

        # -------------------------------------------------
        # IMPORTANT
        #
        # EmployId, Employname aur Salary change nahi
        # kar rahe.
        #
        # Ye attendance create hone ke time employee se
        # save ho chuke hain.
        # -------------------------------------------------

        attendance.save()

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

                "error":
                    "Method not allowed"
            },
            status=405
        )

    # =====================================================
    # GET UNIQUE EMPLOYEE IDS FROM ATTENDANCE
    # =====================================================
    #
    # IMPORTANT:
    #
    # Yahan Employ_Data use nahi ho raha.
    #
    # Salary ka source ATTENDANCE hai.
    #
    # Jis employee ki attendance hai,
    # wahi Salary page me dikhega.
    #
    # =====================================================

    employ_ids = (
        Employ_Att.objects
        .values_list(
            "EmployId",
            flat=True
        )
        .distinct()
        .order_by("EmployId")
    )

    salary_data = []

    # =====================================================
    # CALCULATE SALARY
    # =====================================================

    for employ_id in employ_ids:

        # =================================================
        # ALL ATTENDANCE OF THIS EMPLOYEE
        # =================================================

        attendance = Employ_Att.objects.filter(

            EmployId=employ_id

        ).order_by("Date")

        # =================================================
        # SAFETY CHECK
        # =================================================

        if not attendance.exists():
            continue

        # =================================================
        # FIRST ATTENDANCE
        # =================================================
        #
        # Employee Employ_Data se delete ho chuka ho,
        # tab bhi attendance record available hai.
        #
        # Isliye name aur salary attendance se lenge.
        #
        # =================================================

        first_attendance = attendance.first()

        # =================================================
        # EMPLOYEE NAME
        # =================================================

        employ_name = first_attendance.Employname

        # =================================================
        # MONTHLY SALARY
        # =================================================

        try:

            monthly_salary = float(
                first_attendance.Salary
            )

        except (
            ValueError,
            TypeError
        ):

            monthly_salary = 0

        # =================================================
        # PRESENT COUNT
        # =================================================

        present = attendance.filter(
            Status="Present"
        ).count()

        # =================================================
        # HALF DAY COUNT
        # =================================================

        half_day = attendance.filter(
            Status="Half Day"
        ).count()

        # =================================================
        # ABSENT COUNT
        # =================================================

        absent = attendance.filter(
            Status="Absent"
        ).count()

        # =================================================
        # PER DAY SALARY
        # =================================================

        per_day_salary = (
            monthly_salary / 31
        )

        # =================================================
        # TOTAL SALARY
        # =================================================

        total_salary = (

            present *
            per_day_salary

        ) + (

            half_day *
            0.5 *
            per_day_salary

        )

        # =================================================
        # ADD SALARY DATA
        # =================================================

        salary_data.append({

            "EmployId":
                employ_id,

            "Employname":
                employ_name,

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

    # =====================================================
    # RETURN JSON
    # =====================================================

    return JsonResponse(
        salary_data,
        safe=False
    )