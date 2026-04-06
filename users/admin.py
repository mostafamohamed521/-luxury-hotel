from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'phone', 'is_staff', 'date_joined']
    list_filter = ['is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('phone', 'avatar', 'date_of_birth', 'nationality', 'bio')}),
    )
