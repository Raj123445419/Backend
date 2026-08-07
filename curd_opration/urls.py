"""
URL configuration for curd_opration project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from curd_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Employ_list, name='Employ_list'),
    path('Delete/<int:id>/', views.Delete, name='Delete'),
    path('Edite/<int:id>/', views.Edite, name='Edite'),
    path('Employ_attendance/', views.Employ_attendance, name='Employ_attendance'),
    path('Delete_attendance/<int:id>/', views.Delete_attendance, name='Delete_attendance'),
    path('Edite_attendance/<int:id>/', views.Edite_attendance, name='Edite_attendance'),
    path('Employ_Sallery/', views.Employ_Sallery, name='Employ_Sallery'),













]
