from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from .models import Room, RoomCategory, Review, Favorite, RoomImage
from bookings.forms import SearchForm
from bookings.models import Booking
from services.models import Service, ServiceCategory, GalleryImage
from datetime import date

def home(request):
    featured_rooms = Room.objects.filter(is_featured=True, status='available')[:3]
    categories = RoomCategory.objects.all()
    services = Service.objects.filter(is_featured=True)[:4]
    reviews = Review.objects.select_related('user', 'room').order_by('-created_at')[:6]
    search_form = SearchForm()
    context = {
        'featured_rooms': featured_rooms,
        'categories': categories,
        'services': services,
        'reviews': reviews,
        'search_form': search_form,
        'today': date.today().strftime('%Y-%m-%d'),
    }
    return render(request, 'home/index.html', context)

def rooms_list(request):
    rooms = Room.objects.filter(status='available').prefetch_related('images', 'amenities')
    categories = RoomCategory.objects.all()
    form = SearchForm(request.GET or None)

    if form.is_valid():
        data = form.cleaned_data
        if data.get('guests'):
            rooms = rooms.filter(max_guests__gte=data['guests'])
        if data.get('min_price'):
            rooms = rooms.filter(price_per_night__gte=data['min_price'])
        if data.get('max_price'):
            rooms = rooms.filter(price_per_night__lte=data['max_price'])
        if data.get('category'):
            rooms = rooms.filter(category__slug=data['category'])
        if data.get('sea_view'):
            rooms = rooms.filter(has_sea_view=True)
        if data.get('has_balcony'):
            rooms = rooms.filter(has_balcony=True)
        if data.get('has_jacuzzi'):
            rooms = rooms.filter(has_jacuzzi=True)
        if data.get('check_in') and data.get('check_out'):
            booked_rooms = Booking.objects.filter(
                status__in=['pending', 'confirmed', 'checked_in'],
                check_in__lt=data['check_out'],
                check_out__gt=data['check_in'],
            ).values_list('room_id', flat=True)
            rooms = rooms.exclude(id__in=booked_rooms)

    user_favorites = []
    if request.user.is_authenticated:
        user_favorites = Favorite.objects.filter(user=request.user).values_list('room_id', flat=True)

    context = {
        'rooms': rooms,
        'categories': categories,
        'form': form,
        'user_favorites': list(user_favorites),
    }
    return render(request, 'rooms/list.html', context)

def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    images = room.images.all()
    amenities = room.amenities.all()
    reviews = room.reviews.select_related('user').all()
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, room=room).exists()
    context = {
        'room': room,
        'images': images,
        'amenities': amenities,
        'reviews': reviews,
        'is_favorite': is_favorite,
        'today': date.today().strftime('%Y-%m-%d'),
    }
    return render(request, 'rooms/detail.html', context)

@login_required
def toggle_favorite(request, pk):
    room = get_object_or_404(Room, pk=pk)
    fav, created = Favorite.objects.get_or_create(user=request.user, room=room)
    if not created:
        fav.delete()
        messages.success(request, f"{room.name} removed from your wishlist.")
    else:
        messages.success(request, f"{room.name} added to your wishlist!")
    return redirect(request.META.get('HTTP_REFERER', 'room_detail'))

@login_required
def add_review(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        if Review.objects.filter(room=room, user=request.user).exists():
            messages.error(request, "You have already reviewed this room.")
        else:
            Review.objects.create(
                room=room,
                user=request.user,
                rating=int(request.POST.get('rating', 5)),
                title=request.POST.get('title', ''),
                comment=request.POST.get('comment', ''),
                cleanliness=int(request.POST.get('cleanliness', 5)),
                service=int(request.POST.get('service', 5)),
                comfort=int(request.POST.get('comfort', 5)),
            )
            messages.success(request, "Your review has been submitted. Thank you!")
    return redirect('room_detail', pk=pk)

def gallery(request):
    images = GalleryImage.objects.all()
    categories = dict(GalleryImage.CATEGORY_CHOICES)
    selected = request.GET.get('cat', 'all')
    if selected != 'all':
        images = images.filter(category=selected)
    return render(request, 'gallery/gallery.html', {'images': images, 'categories': categories, 'selected': selected})

def services_page(request):
    service_categories = ServiceCategory.objects.prefetch_related('services').all()
    return render(request, 'services/services.html', {'service_categories': service_categories})

def about(request):
    return render(request, 'about/about.html')

def contact(request):
    if request.method == 'POST':
        messages.success(request, "Your message has been sent. We'll be in touch within 24 hours.")
        return redirect('contact')
    return render(request, 'contact/contact.html')
