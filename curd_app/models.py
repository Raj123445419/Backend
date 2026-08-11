from django.db import models

# Create your models here.
class Employ_Data(models.Model):
    EmployId=models.AutoField(primary_key=True)
    Employname=models.CharField(max_length=50000)
    Address=models.CharField(max_length=200000)
    Employrole=models.CharField(max_length=50000)
    Designation=models.CharField(max_length=50000)
    Experince=models.CharField(max_length=20000)
    Salary=models.CharField(max_length=2000000000000000000000000000000000000000000000000000000000000000000000000000000000000000)

    def __str__(self):
        return str(self.EmployId)





class Employ_Att(models.Model):
    EmployId = models.IntegerField()
    Employname = models.CharField(max_length=50)
    Date = models.DateField()
    Status = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.EmployId} - {self.Employname}"


