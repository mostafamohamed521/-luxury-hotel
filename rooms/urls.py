from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rooms/', views.rooms_list, name='rooms_list'),
    path('rooms/<int:pk>/', views.room_detail, name='room_detail'),
    path('rooms/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('rooms/<int:pk>/review/', views.add_review, name='add_review'),
    path('gallery/', views.gallery, name='gallery'),
    path('services/', views.services_page, name='services'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]

from . import admin_views
urlpatterns += [
    path('admin-panel/', admin_views.dashboard, name='admin_dashboard'),
    path('admin-panel/rooms/', admin_views.admin_rooms, name='admin_rooms'),
    path('admin-panel/bookings/', admin_views.admin_bookings, name='admin_bookings'),
    path('admin-panel/users/', admin_views.admin_users, name='admin_users'),
    path('admin-panel/payments/', admin_views.admin_payments, name='admin_payments'),
    path('admin-panel/bookings/<int:pk>/status/', admin_views.update_booking_status, name='update_booking_status'),
]
