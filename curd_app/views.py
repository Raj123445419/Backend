from urllib import request
from django.shortcuts import redirect, render
from curd_app.models import Employ_Data

# Create your views here.
from django.shortcuts import render, redirect
from .models import Employ_Att, Employ_Data











def Employ_list(request):

    if request.method == "POST":

        Employ_Data.objects.create(
            Employname=request.POST['Employname'],
            Address=request.POST['Address'],
            Employrole=request.POST['Employrole'],
            Designation=request.POST['Designation'],
            Experince=request.POST['Experince'],
            Salary=request.POST['Salary'],
        )

        return redirect('Employ_list')

    data = Employ_Data.objects.all()

    return render(request, 'Employ_list.html', {
        'data': data
    })

# def Add_employ(request):
#       return render(request, 'Add_employ.html')



def Delete(request,id):

    employee = Employ_Data.objects.get(EmployId=id)

    employee.delete()

    return redirect('Employ_list')



def Edite(request, id):


    employee = Employ_Data.objects.get(EmployId=id)


    if request.method == "POST":

        employee.Employname = request.POST.get('Employname')
        employee.Address = request.POST.get('Address')
        employee.Employrole = request.POST.get('Employrole')
        employee.Designation = request.POST.get('Designation')
        employee.Experince = request.POST.get('Experince')
        employee.Salary = request.POST.get('Salary')

        employee.save()

        return redirect('Employ_list')

    return render(request, 'Edite.html', {
        'employee': employee
    })





def Employ_attendance(request):

    if request.method == "POST":

        try:
            emp = Employ_Data.objects.get(
                EmployId=request.POST['EmployId']
            )

            date = request.POST['Date']
            status = request.POST['Status']

            attendance = Employ_Att.objects.filter(
                EmployId=emp.EmployId,
                Date=date
            ).first()

            if attendance:
                return render(request, 'Employ_attendance.html', {
                    'attendance': Employ_Att.objects.all(),
                    'error': 'This employee attendance is already marked for this date.'
                })

            Employ_Att.objects.create(
                EmployId=emp.EmployId,
                Employname=emp.Employname,
                Date=date,
                Status=status
            )

            return redirect('Employ_attendance')

        except Employ_Data.DoesNotExist:
            return render(request, 'Employ_attendance.html', {
                'attendance': Employ_Att.objects.all(),
                'error': 'Employee ID not found.'
            })

    attendance = Employ_Att.objects.all()

    return render(request, 'Employ_attendance.html', {
        'attendance': attendance
    })





def Delete_attendance(request, id):

    Employ_Att.objects.filter(id=id).delete()

    return redirect('Employ_attendance')




def Employ_sallery(request):

    employees = Employ_Data.objects.all()
    salary_data = []

    for emp in employees:

        # Attendance Count
        present = Employ_Att.objects.filter(
            EmployId=emp.EmployId,
            Status="Present"
        ).count()

        half_day = Employ_Att.objects.filter(
            EmployId=emp.EmployId,
            Status="Half Day"
        ).count()

        absent = Employ_Att.objects.filter(
            EmployId=emp.EmployId,
            Status="Absent"
        ).count()


        monthly_salary = float(emp.Salary)

        per_day_salary = monthly_salary / 31

    
        total_salary = (
            (present * per_day_salary) +
            (half_day * 0.5 * per_day_salary)
        )

        salary_data.append({
            "EmployId": emp.EmployId,
            "Employname": emp.Employname,
            "Salary": monthly_salary,
            "Present": present,
            "HalfDay": half_day,
            "Absent": absent,
            "TotalSalary": round(total_salary, 2),
        })

    return render(request, "Employ_sallery.html", {
        "salary_data": salary_data
    })




def Edite_attendance(request, id):

    attendance = Employ_Att.objects.filter(id=id).first()

    if attendance is None:
        return redirect('Employ_attendance')

    if request.method == "POST":

        attendance.Date = request.POST['Date']
        attendance.Status = request.POST['Status']

        attendance.save()

        return redirect('Employ_attendance')

    return render(request, 'Edite_attendance.html', {
        'attendance': attendance
    })




