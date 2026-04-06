from django.db import models
from django.contrib.auth import get_user_model
from rooms.models import Room
from decimal import Decimal
import uuid

User = get_user_model()

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
    ]
    booking_ref = models.CharField(max_length=20, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True)
    nights = models.PositiveIntegerField(editable=False, default=0)
    room_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)
    taxes = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.booking_ref:
            self.booking_ref = f"LUM{uuid.uuid4().hex[:8].upper()}"
        self.nights = (self.check_out - self.check_in).days
        self.room_price = self.room.price_per_night * self.nights
        self.taxes = self.room_price * Decimal('0.15')
        self.total_price = self.room_price + self.taxes
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.booking_ref} - {self.user.email}"

    class Meta:
        ordering = ['-created_at']
