from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileUpdateForm
from rooms.models import Favorite

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f"Welcome to Lumière, {user.first_name}! Your account has been created.")
        return redirect('home')
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f"Welcome back, {user.first_name}!")
        return redirect(request.GET.get('next', 'home'))
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been signed out. We look forward to welcoming you back.")
    return redirect('home')

@login_required
def profile_view(request):
    bookings = request.user.bookings.select_related('room').order_by('-created_at')
    favorites = Favorite.objects.filter(user=request.user).select_related('room')
    return render(request, 'users/profile.html', {'bookings': bookings, 'favorites': favorites})

@login_required
def edit_profile(request):
    form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('profile')
    return render(request, 'users/edit_profile.html', {'form': form})

@login_required
def wishlist_view(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('room').prefetch_related('room__images')
    return render(request, 'users/wishlist.html', {'favorites': favorites})
