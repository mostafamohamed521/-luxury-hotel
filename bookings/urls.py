from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:room_pk>/', views.create_booking, name='create_booking'),
    path('<int:pk>/', views.booking_detail, name='booking_detail'),
    path('<int:pk>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
]
