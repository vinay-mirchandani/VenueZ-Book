from django.contrib import admin
from django.urls import path

from client import client_views

urlpatterns = [

    path('Home/', client_views.home),

    path('log/', client_views.c_login),
    path('reg/', client_views.c_register),
    path('forgot/', client_views.forgot_password),

    path('about-us/', client_views.about_us),
    path('destination/<int:pckg_id>/', client_views.c_destination),
    path('hall_details/<int:hall_id>/', client_views.hall_details),

    path('feedback/', client_views.c_feedback),

    path('My_Bookings/', client_views.cart),


    path('error/', client_views.error404),

    path('booking/<int:pckg_id>/', client_views.booking),
    path('confirm_booking/<int:pckg_id>/', client_views.select_checkout),

    path('venues/<int:category_id>/', client_views.venues),
    path('venuez/', client_views.venuez),

    path('owner_reg/',client_views.owner_register),
    path('owner_log/',client_views.owner_login),

    path('faq/', client_views.FAQ),
    path('contact/', client_views.contact),
    path('client_header_menu/', client_views.load_menu),

    path('packages/<int:package_id>/', client_views.packages),
    path('single/<int:package_id>/', client_views.c_package),
    path('search1/', client_views.autosuggest, name='search1'),
    path('show/', client_views.showhall),

    path('sendOTP/',client_views.send_otp),
    path('reset/',client_views.set_password),

    path('sendootp/', client_views.send_oOtp),
    path('owner_reset/',client_views.resetowner),
    path('oforgot/',client_views.owner_forgot),

]
