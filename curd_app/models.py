# from django.db import models

# # Create your models here.
# # class Employ_Data(models.Model):
# #     EmployId=models.AutoField(primary_key=True)
# #     Employname=models.CharField(max_length=50000)
# #     Address=models.CharField(max_length=5000)
# #     Employrole=models.CharField(max_length=50000)
# #     Designation=models.CharField(max_length=50000)
# #     Experince=models.CharField(max_length=50000)
# #     Salary=models.CharField(max_length=50000)

# #     def __str__(self):
# #         return str(self.EmployId)



# class Employ_Data(models.Model):
#     EmployId = models.AutoField(primary_key=True)
#     Employname = models.TextField()
#     Address = models.TextField()
#     Employrole = models.TextField()
#     Designation = models.TextField()
#     Experince = models.TextField()
#     Salary = models.TextField()

#     def __str__(self):
#         return str(self.EmployId)

# class Employ_Att(models.Model):
#     EmployId = models.IntegerField()
#     Employname = models.CharField(max_length=50000)
#     Date = models.DateField()
#     Status = models.CharField(max_length=20000)

#     def __str__(self):
#         return f"{self.EmployId} - {self.Employname}"

from django.db import models


# =========================================================
# EMPLOYEE MODEL
# =========================================================

class Employ_Data(models.Model):

    EmployId = models.AutoField(
        primary_key=True
    )

    Employname = models.TextField()

    Address = models.TextField()

    Employrole = models.TextField()

    Designation = models.TextField()

    Experince = models.TextField()

    Salary = models.TextField()

    def __str__(self):

        return str(self.EmployId)


# =========================================================
# ATTENDANCE MODEL
# =========================================================

class Employ_Att(models.Model):

    id = models.AutoField(
        primary_key=True
    )

    EmployId = models.IntegerField()

    Employname = models.CharField(
        max_length=50000
    )

    Date = models.DateField()

    Status = models.CharField(
        max_length=20000
    )

    def __str__(self):

        return f"{self.EmployId} - {self.Employname}"


# =========================================================
# SALARY MODEL
#
# IMPORTANT:
# Employee delete hone ke baad bhi salary record rahega.
# =========================================================

class Employ_Salary(models.Model):

    id = models.AutoField(
        primary_key=True
    )

    # Employee ka ID
    EmployId = models.IntegerField()

    # Employee ka naam
    Employname = models.CharField(
        max_length=50000
    )

    # Monthly salary
    MonthlySalary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    # Salary record kis month/year ka hai
    Month = models.IntegerField()

    Year = models.IntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.EmployId} - "
            f"{self.Employname} - "
            f"{self.Month}/{self.Year}"
        )