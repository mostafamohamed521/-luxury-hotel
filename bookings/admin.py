from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_ref', 'user', 'room', 'check_in', 'check_out', 'status', 'total_price']
    list_filter = ['status']
    search_fields = ['booking_ref', 'user__email']
    readonly_fields = ['booking_ref', 'nights', 'room_price', 'taxes', 'total_price']
