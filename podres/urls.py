from django.urls import path
from .views import room_list, book_room, booking_list, booking_detail

urlpatterns = [
    path('', room_list, name='room_list'),
    path('book/<int:room_id>/', book_room, name='book_room'),
    path('bookings/', booking_list, name='booking_list'),
    path('booking/<int:booking_id>/', booking_detail, name='booking_detail'),
]
