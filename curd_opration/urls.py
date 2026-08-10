
from django.contrib import admin
from django.urls import path

from curd_app import views


urlpatterns = [

    # =====================================================
    # ADMIN
    # =====================================================

    path(
        "admin/",
        admin.site.urls
    ),


    # =====================================================
    # EMPLOYEE
    # =====================================================

    # GET  -> Employee list
    # POST -> Add employee
    path(
        "",
        views.Employ_list,
        name="Employ_list"
    ),

    # DELETE employee
    path(
        "Delete/<int:id>/",
        views.Delete,
        name="Delete"
    ),

    # GET / POST employee edit
    path(
        "Edite/<int:id>/",
        views.Edite,
        name="Edite"
    ),


    # =====================================================
    # ATTENDANCE
    # =====================================================

    # GET  -> Attendance list
    # POST -> Add attendance
    path(
        "Employ_attendance/",
        views.Employ_attendance,
        name="Employ_attendance"
    ),

    # DELETE attendance
    path(
        "Delete_attendance/<int:id>/",
        views.Delete_attendance,
        name="Delete_attendance"
    ),

    # GET / POST attendance edit
    path(
        "Edite_attendance/<int:id>/",
        views.Edite_attendance,
        name="Edite_attendance"
    ),


    # =====================================================
    # SALARY
    # =====================================================

    # GET -> Salary calculation
    path(
        "Employ_Sallery/",
        views.Employ_Sallery,
        name="Employ_Sallery"
    ),
]

