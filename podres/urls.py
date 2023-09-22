from django.urls import path
from podres.views.views import *
from podres.views.servicedetail import ServiceDetailView
from podres.views.createbooking import CreateBookingView
from podres.views.deletebooking import DeleteBookingView
from podres.views.auth import *
from podres.views.bookinglist import BookingListView
from podres.views.bans_list import BansListView
from podres.views.profile import ProfileView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', home, name='home'),
    path('services/', service_list, name='service_list'),
    path('accounts/profile/', ProfileView.as_view(), name='profile'),
    path('about/', about, name='about'),
    path('bookings/', BookingListView.as_view(), name='booking_list'),
    path('users/', user_list, name='user_list'),
    path('bans/', BansListView.as_view(), name='bans_list'),
    path('service/<int:pk>/', ServiceDetailView.as_view(), name='service_detail'),
    path('booking/<int:pk>/', booking_detail, name='booking_detail'),
    path('user/<int:pk>/', user_detail, name='user_detail'),

    #redirects
    path('deletebooking/<int:pk>/', DeleteBookingView.as_view(), name='delete_booking'),
    path('createbooking/<int:serviceid>/<int:day>/<int:month>/<int:year>/<int:hour>', CreateBookingView.as_view(), name='create_booking'),
    path('langchange/<str:lang_code>', change_language, name='change_language'),

    # Authentication
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
    path('accounts/password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
