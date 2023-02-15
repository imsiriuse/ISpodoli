from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Room, Booking, RoomType


def room_list(request):
    rooms = Room.objects.filter(is_available=True)
    return render(request, 'room_list.html', {'rooms': rooms})


def book_room(request, room_id):
    room = Room.objects.get(id=room_id)
    if not room.is_available:
        return redirect('room_list')

    if request.method == 'POST':
        start_date = timezone.datetime.strptime(request.POST['start_date'], '%Y-%m-%d').date()
        end_date = timezone.datetime.strptime(request.POST['end_date'], '%Y-%m-%d').date()
        booking = Booking(room=room, user=request.user, start_date=start_date, end_date=end_date)
        booking.save()
        room.is_available = False
        room.save()
        return redirect('booking_detail', booking_id=booking.id)
    else:
        return render(request, 'book_room.html', {'room': room})


def booking_list(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking_list.html', {'bookings': bookings})


def booking_detail(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if booking.user != request.user:
        return redirect('booking_list')
    return render(request, 'booking_detail.html', {'booking': booking})

