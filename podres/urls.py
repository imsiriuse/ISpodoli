from django.urls import path
from .views import *

urlpatterns = [
    path('', service_list, name='service_list'),
    path('service/<int:service_id>/', service_detail, name='service_detail'),
    path('bookings/', booking_list, name='booking_list'),
    path('booking/<int:booking_id>/', booking_detail, name='booking_detail'),
    path('rooms/', rooms_list, name='rooms_list'),
    path('bookings/delete/<int:booking_id>/', delete_booking, name='delete_booking'),
    path('service/create_booking/<int:service_id>/', create_booking, name='create_booking'),
]
