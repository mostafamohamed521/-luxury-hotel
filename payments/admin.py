from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'booking', 'amount', 'method', 'status', 'created_at']
    list_filter = ['status', 'method']
    readonly_fields = ['payment_id']
