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
