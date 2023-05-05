from django.urls import path
from podres.views.views import *
from .views.servicedetail import ServiceDetailView
from .views.createbooking import CreateBookingView


urlpatterns = [
    path('', homepage, name='homepage'),
    path('accounts/profile/', profile, name='profile'),
    path('services/', service_list, name='service_list'),
    path('about/', about, name='about'),
    path('bookings/', booking_list, name='booking_list'),
    path('service/<int:pk>/', ServiceDetailView.as_view(), name='service_detail'),
    path('booking/<int:pk>/', booking_detail, name='booking_detail'),
    path('bookings/delete/<int:pk>/', delete_booking, name='delete_booking'),
    path('createbooking/<int:service>/<int:day>/<int:month>/<int:year>/<int:hour>', CreateBookingView.as_view(), name='create_booking'),
]
