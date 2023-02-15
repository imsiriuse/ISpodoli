from django.urls import path
from .views import *

urlpatterns = [
    path('', service_list, name='room_list'),
    path('room/<int:room_id>/', room_detail, name='room_detail'),
    path('book/<int:room_id>/', book_room, name='book_room'),
    path('bookings/', booking_list, name='booking_list'),
    path('booking/<int:booking_id>/', booking_detail, name='booking_detail'),
]
