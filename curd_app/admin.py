from django.contrib import admin

from curd_app.models import Employ_Att, Employ_Data, Employ_Salary 

# Register your models here.
admin.site.register(Employ_Data)
admin.site.register(Employ_Att)
admin.site.register(Employ_Salary)
