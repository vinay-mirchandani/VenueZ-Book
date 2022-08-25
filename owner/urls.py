from django.contrib import admin
from django.urls import path, include
from owner import owner_views
from django.conf.urls import url
from fly.views import  HomeView , ClientChart
urlpatterns = [

    path('owner_dashboard/',owner_views.owner_dashboard),
    path('all_hall/',owner_views.show_hall),

    path('owner_order_accepted/<int:id>/',owner_views.order_accepted),
    path('owner_order_rejected/<int:id>/',owner_views.order_rejected),

    path('del_booking/<int:id>/', owner_views.del_booking),
    path('owner_area/', owner_views.owner_area),

    path('owner_edit/', owner_views.owner_edit),
    path('owner_update/', owner_views.owner_update),

    path('owner_package/', owner_views.owner_package),
    path('owner_report1/', owner_views.report1),
    path('owner_report2/', owner_views.report2),
    path('owner_gallery/', owner_views.gallery_view ),

]