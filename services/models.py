from django.db import models

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Service Categories'

class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    duration = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class GalleryImage(models.Model):
    CATEGORY_CHOICES = [
        ('rooms', 'Rooms'),
        ('spa', 'Spa'),
        ('restaurant', 'Restaurant'),
        ('pool', 'Pool'),
        ('exterior', 'Exterior'),
        ('events', 'Events'),
    ]
    image = models.ImageField(upload_to='gallery/')
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
