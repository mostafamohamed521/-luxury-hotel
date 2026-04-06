from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class RoomCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='bed')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Room Categories'

class Room(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
    ]
    category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=200)
    room_number = models.CharField(max_length=10, unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    max_guests = models.PositiveIntegerField(default=2)
    size_sqm = models.PositiveIntegerField()
    floor = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    is_featured = models.BooleanField(default=False)
    has_sea_view = models.BooleanField(default=False)
    has_balcony = models.BooleanField(default=False)
    has_jacuzzi = models.BooleanField(default=False)
    has_fireplace = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - Room {self.room_number}"

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0

    def review_count(self):
        return self.reviews.count()

class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='rooms/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

class RoomAmenity(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='amenities')
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default='check')

    def __str__(self):
        return self.name

class Review(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200)
    comment = models.TextField()
    cleanliness = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=5)
    service = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=5)
    comfort = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('room', 'user')
        ordering = ['-created_at']

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'room')
