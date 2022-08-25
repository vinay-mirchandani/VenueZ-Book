"""Revision URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from fly import views
from django.conf.urls import url
from fly.views import  HomeView , ClientChart


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', views.view),

    path('register/',views.register),
    path('login/', views.admin_login),
    path('logout/', views.logout),

    path('forgot/', views.forgot),
    path('sendmail/', views.send_otp),
    path('resetpass/', views.set_password),

    path('edit_profile/', views.admin_edit),
    path('update_profile/', views.admin_update),

    path('insert_are/', views.insert_are),
    path('Area/', views.show_area),
    path('update_area/<int:area_id>/',  views.update_area),
    path('edit_are/<int:area_id>/', views.edit_area),
    path('del_area/<int:id>/',views.delete_area),

    path('insert_category/', views.category),
    path('show_category/',views.show_category),

    path('insert_hall/', views.hall),
    path('show_halls/',views.show_hall),

    path('gallery/',views.gallery_insert),
    path('dashboard/',views.dashboard),

    path('gallery_view/',views.gallery_view),
    path('del_booking/<int:id>/',views.del_booking),
    path('order_accepted/<int:id>/',views.order_accepted),
    path('order_rejected/<int:id>/',views.order_rejected),



    url(r'doctorhome', HomeView.as_view(), name='home'),
    url(r'^api/chart/data/$', ClientChart.as_view(),name="api-data"),

    path('show_packages/', views.show_package),
    path('insert_packages/', views.insert_package),

    path('booking/', views.booking),
    path('booking_report1/', views.report1),
    path('booking_report2/', views.report2),
    path('booking_report3/', views.report3),

    path('client/', include('client.urls')),
    path('owner/', include('owner.urls')),


]
