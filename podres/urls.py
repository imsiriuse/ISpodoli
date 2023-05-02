from django.urls import path
from .views import *

urlpatterns = [
    path('', service_list, name='service_list'),
    path('rooms/', rooms_list, name='rooms_list'),
    path('bookings/', booking_list, name='booking_list'),
    path('service/<int:pk>/', service_detail, name='service_detail'),

    path('booking/<int:pk>/', booking_detail, name='booking_detail'),
    path('bookings/delete/<int:pk>/', delete_booking, name='delete_booking'),
    path('service/create/<int:pk>/', create_booking, name='create_booking'),
]
