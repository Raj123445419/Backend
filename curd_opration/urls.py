
from django.contrib import admin
from django.urls import path

from curd_app import views


urlpatterns = [

    # =====================================================
    # ADMIN
    # =====================================================

    path(
        "admin/",admin.site.urls
    ),

    path(
        "",
        views.Employ_list,name="Employ_list"
    ),


    path(
        "Delete/<int:id>/",views.Delete,name="Delete"
    ),


    path(
        "Edite/<int:id>/",views.Edite,name="Edite"
    ),


    path(
        "Employ_attendance/",views.Employ_attendance,name="Employ_attendance"
    ),


    path(
        "Delete_attendance/<int:id>/",views.Delete_attendance,name="Delete_attendance"
    ),


    path(
        "Edite_attendance/<int:id>/",views.Edite_attendance,name="Edite_attendance"
    ),


    path(
        "Employ_Sallery/",views.Employ_Sallery,name="Employ_Sallery"
    ),

path('mark-attendance/', views.mark_attendance_via_qr, name='mark_attendance'),

]

