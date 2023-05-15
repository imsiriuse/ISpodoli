from django.urls import path
from podres.views.views import *
from .views.servicedetail import ServiceDetailView
from .views.createbooking import CreateBookingView
from .views.deletebooking import DeleteBookingView
from .views.bookinglist import BookingListView
from .views.bookinghistory import BookingHistoryView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', service_list, name='service_list'),
    path('accounts/profile/', profile, name='profile'),
    path('about/', about, name='about'),
    path('bookings/', BookingListView.as_view(), name='booking_list'),
    path('service/<int:pk>/', ServiceDetailView.as_view(), name='service_detail'),
    path('bookings/delete/<int:pk>/', DeleteBookingView.as_view(), name='delete_booking'),
    path('createbooking/<int:serviceid>/<int:day>/<int:month>/<int:year>/<int:hour>', CreateBookingView.as_view(), name='create_booking'),
    path('booking_history/', BookingHistoryView.as_view(), name='booking_history'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)