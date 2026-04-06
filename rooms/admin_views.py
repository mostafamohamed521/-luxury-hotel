from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from rooms.models import Room, RoomCategory, Review
from bookings.models import Booking
from payments.models import Payment
from django.contrib.auth import get_user_model

User = get_user_model()

@staff_member_required
def dashboard(request):
    today = timezone.now().date()
    month_start = today.replace(day=1)
    
    total_revenue = Payment.objects.filter(status='completed').aggregate(t=Sum('amount'))['t'] or 0
    month_revenue = Payment.objects.filter(status='completed', created_at__date__gte=month_start).aggregate(t=Sum('amount'))['t'] or 0
    total_bookings = Booking.objects.count()
    active_bookings = Booking.objects.filter(status__in=['confirmed', 'checked_in']).count()
    total_users = User.objects.count()
    total_rooms = Room.objects.count()
    available_rooms = Room.objects.filter(status='available').count()
    
    recent_bookings = Booking.objects.select_related('user', 'room').order_by('-created_at')[:10]
    booking_stats = Booking.objects.values('status').annotate(count=Count('id'))
    
    monthly_revenue = []
    for i in range(6):
        m = today - timedelta(days=30*i)
        rev = Payment.objects.filter(
            status='completed',
            created_at__year=m.year,
            created_at__month=m.month
        ).aggregate(t=Sum('amount'))['t'] or 0
        monthly_revenue.append({'month': m.strftime('%b %Y'), 'revenue': float(rev)})
    
    context = {
        'total_revenue': total_revenue,
        'month_revenue': month_revenue,
        'total_bookings': total_bookings,
        'active_bookings': active_bookings,
        'total_users': total_users,
        'total_rooms': total_rooms,
        'available_rooms': available_rooms,
        'recent_bookings': recent_bookings,
        'booking_stats': list(booking_stats),
        'monthly_revenue': list(reversed(monthly_revenue)),
    }
    return render(request, 'admin_dashboard/dashboard.html', context)

@staff_member_required
def admin_rooms(request):
    rooms = Room.objects.select_related('category').prefetch_related('images').all()
    return render(request, 'admin_dashboard/rooms.html', {'rooms': rooms})

@staff_member_required
def admin_bookings(request):
    bookings = Booking.objects.select_related('user', 'room').all()
    status_filter = request.GET.get('status', '')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    return render(request, 'admin_dashboard/bookings.html', {'bookings': bookings, 'status_filter': status_filter})

@staff_member_required
def admin_users(request):
    users = User.objects.annotate(booking_count=Count('bookings')).order_by('-date_joined')
    return render(request, 'admin_dashboard/users.html', {'users': users})

@staff_member_required
def admin_payments(request):
    payments = Payment.objects.select_related('booking__user', 'booking__room').order_by('-created_at')
    return render(request, 'admin_dashboard/payments.html', {'payments': payments})

@staff_member_required
def update_booking_status(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Booking.STATUS_CHOICES):
            booking.status = new_status
            booking.save()
            messages.success(request, f"Booking {booking.booking_ref} updated to {new_status}.")
    return redirect('admin_bookings')
