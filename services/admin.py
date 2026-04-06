from django.contrib import admin
from .models import ServiceCategory, Service, GalleryImage

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'is_featured']
    list_filter = ['category', 'is_available', 'is_featured']

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'order']
