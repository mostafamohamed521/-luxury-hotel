from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rooms.models import Room
from .models import Booking
from .forms import BookingForm

@login_required
def create_booking(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk, status='available')
    form = BookingForm(room=room, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        booking = form.save(commit=False)
        booking.user = request.user
        booking.room = room
        booking.save()
        messages.success(request, f"Booking created! Reference: {booking.booking_ref}")
        return redirect('checkout', booking_pk=booking.pk)
    return render(request, 'bookings/create.html', {'room': room, 'form': form})

@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'bookings/detail.html', {'booking': booking})

@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if booking.status in ['pending', 'confirmed']:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, f"Booking {booking.booking_ref} has been cancelled.")
    else:
        messages.error(request, "This booking cannot be cancelled.")
    return redirect('my_bookings')

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('room').order_by('-created_at')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})
