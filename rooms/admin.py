from django.contrib import admin
from .models import Room, RoomCategory, RoomImage, RoomAmenity, Review, Favorite

class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1

class RoomAmenityInline(admin.TabularInline):
    model = RoomAmenity
    extra = 1

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'name', 'category', 'price_per_night', 'status', 'is_featured']
    list_filter = ['status', 'category', 'is_featured']
    search_fields = ['name', 'room_number']
    inlines = [RoomImageInline, RoomAmenityInline]

@admin.register(RoomCategory)
class RoomCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Review)
admin.site.register(Favorite)
