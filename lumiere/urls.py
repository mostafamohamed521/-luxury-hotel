from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', include('rooms.urls')),
    path('users/', include('users.urls')),
    path('bookings/', include('bookings.urls')),
    path('payments/', include('payments.urls')),
    path('services/', include('services.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
