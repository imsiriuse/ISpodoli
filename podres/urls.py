from django.urls import path
from podres.views.views import *
from .views.servicedetail import ServiceDetailView
from .views.createbooking import CreateBookingView
from .views.deletebooking import DeleteBookingView
from .views.bookinglist import BookingListView
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', service_list, name='service_list'),
    path('accounts/profile/', TemplateView.as_view(template_name='static/profile.html'), name='profile'),
    path('about/', TemplateView.as_view(template_name='static/about.html'), name='about'),
    path('bookings/', BookingListView.as_view(), name='booking_list'),
    path('service/<int:pk>/', ServiceDetailView.as_view(), name='service_detail'),
    path('bookings/delete/<int:pk>/', DeleteBookingView.as_view(), name='delete_booking'),
    path('createbooking/<int:serviceid>/<int:day>/<int:month>/<int:year>/<int:hour>', CreateBookingView.as_view(), name='create_booking'),
    path('booking_history/', booking_history, name='booking_history'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)