from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from rooms.models import Room, RoomCategory, RoomAmenity
from services.models import ServiceCategory, Service

User = get_user_model()

CATEGORIES = [
    {'name': 'Classic Room', 'slug': 'classic', 'description': 'Elegant rooms with classic Parisian charm'},
    {'name': 'Deluxe Room', 'slug': 'deluxe', 'description': 'Spacious rooms with premium amenities'},
    {'name': 'Junior Suite', 'slug': 'junior-suite', 'description': 'Stylish suites with separate living areas'},
    {'name': 'Grand Suite', 'slug': 'grand-suite', 'description': 'Opulent suites with panoramic city views'},
    {'name': 'Presidential Suite', 'slug': 'presidential', 'description': 'The ultimate expression of luxury'},
]

ROOMS = [
    {'name': 'Haussmann Classic', 'number': '101', 'cat': 'classic', 'price': 320, 'size': 28, 'max': 2, 'floor': 1,
     'short': 'A beautifully appointed classic room with hardwood floors and bespoke furniture.', 'featured': False,
     'desc': 'Inspired by the golden age of Parisian architecture, the Haussmann Classic room blends antique charm with modern comfort. Features include a king-size bed, marble bathroom, and views of the inner courtyard.'},
    {'name': 'Lumiere Deluxe', 'number': '205', 'cat': 'deluxe', 'price': 520, 'size': 38, 'max': 2, 'floor': 2,
     'short': 'Spacious deluxe room with city views and luxury bathroom.', 'featured': True, 'balcony': True,
     'desc': 'The Lumiere Deluxe room offers a generous space adorned with carefully selected art and premium materials. Step onto your private balcony for breathtaking views of the Parisian skyline.'},
    {'name': 'Montmartre Junior Suite', 'number': '314', 'cat': 'junior-suite', 'price': 780, 'size': 55, 'max': 3, 'floor': 3,
     'short': 'Elegant junior suite with separate living area and sea views.', 'featured': True, 'sea': True, 'balcony': True,
     'desc': 'Named after the iconic Paris neighbourhood, this junior suite features a sunlit living room, an oversized king bedroom, and a spa-like bathroom with a freestanding soaking tub.'},
    {'name': 'Belle Epoque Suite', 'number': '412', 'cat': 'grand-suite', 'price': 1200, 'size': 80, 'max': 4, 'floor': 4,
     'short': 'Grand suite with sweeping panoramic views and private butler service.', 'featured': True, 'sea': True, 'balcony': True, 'jacuzzi': True,
     'desc': 'An ode to the Belle Epoque era, this magnificent suite features hand-painted ceilings, custom silk drapes, and a panoramic terrace. Complete with a dedicated butler, private dining room, and jacuzzi terrace.'},
    {'name': 'Champs-Elysees Grand', 'number': '308', 'cat': 'grand-suite', 'price': 950, 'size': 70, 'max': 3, 'floor': 3,
     'short': 'Magnificent grand suite overlooking iconic Parisian landmarks.', 'featured': False, 'sea': True,
     'desc': 'Positioned to offer the most iconic views in Paris, this grand suite features exquisite furnishings, a walk-in wardrobe, and a dual-aspect bathroom with both shower and deep-soak tub.'},
    {'name': 'Presidential Suite', 'number': '501', 'cat': 'presidential', 'price': 3500, 'size': 200, 'max': 6, 'floor': 5,
     'short': 'The pinnacle of luxury — a full-floor private residence in the sky.', 'featured': True, 'sea': True, 'balcony': True, 'jacuzzi': True, 'fire': True,
     'desc': 'Our Presidential Suite occupies the entire fifth floor — a private residence of extraordinary proportions. Three bedrooms, a formal dining room, a private spa, a rooftop terrace, and a dedicated team of staff ensure an experience of unmatched grandeur.'},
]

AMENITIES = ['King Bed', 'High-Speed WiFi', 'Nespresso Machine', 'Mini Bar', 'Flat-Screen TV', 'In-Room Safe', 
             'Air Conditioning', 'Bathrobe & Slippers', 'Premium Toiletries', 'Daily Housekeeping',
             'Turndown Service', 'Room Service 24/7']

SVC_CATS = [
    {'name': 'Wellness & Spa', 'slug': 'spa', 'icon': 'fa-spa', 'description': 'Rejuvenate body and mind'},
    {'name': 'Dining', 'slug': 'dining', 'icon': 'fa-utensils', 'description': 'Culinary excellence'},
    {'name': 'Recreation', 'slug': 'recreation', 'icon': 'fa-swimming-pool', 'description': 'Fitness and leisure'},
    {'name': 'Concierge', 'slug': 'concierge', 'icon': 'fa-concierge-bell', 'description': 'Personal assistance'},
]

SERVICES = [
    {'cat': 'spa', 'name': 'Signature Massage', 'desc': '90-minute full body massage combining Swedish and hot stone techniques.', 'price': 220, 'dur': '90 min', 'featured': True},
    {'cat': 'spa', 'name': 'Lumiere Facial', 'desc': 'A bespoke facial using La Mer products tailored to your skin type.', 'price': 180, 'dur': '60 min', 'featured': True},
    {'cat': 'spa', 'name': 'Couples Ritual', 'desc': 'A romantic 2-hour journey for two in our private couples suite.', 'price': 480, 'dur': '120 min', 'featured': False},
    {'cat': 'dining', 'name': 'Breakfast in Bed', 'desc': 'A lavish breakfast served in your suite — croissants, fresh fruit, champagne.', 'price': 85, 'featured': True},
    {'cat': 'dining', 'name': 'Private Chef Dinner', 'desc': 'An exclusive 5-course dinner prepared by our executive chef in your suite.', 'price': 450, 'featured': True},
    {'cat': 'recreation', 'name': 'Rooftop Yoga', 'desc': 'Morning yoga on our rooftop with panoramic Parisian views.', 'price': 60, 'dur': '60 min', 'featured': False},
    {'cat': 'concierge', 'name': 'Private Airport Transfer', 'desc': 'Chauffeur-driven luxury vehicle to/from CDG or Orly airport.', 'price': 140, 'featured': False},
]

class Command(BaseCommand):
    help = 'Seed the database with sample hotel data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # Superuser
        if not User.objects.filter(email='admin@lumiere-hotel.com').exists():
            User.objects.create_superuser(
                username='admin', email='admin@lumiere-hotel.com',
                password='admin123', first_name='Hotel', last_name='Admin'
            )
            self.stdout.write('  Created superuser: admin@lumiere-hotel.com / admin123')

        # Test guest
        if not User.objects.filter(email='guest@example.com').exists():
            User.objects.create_user(
                username='guest', email='guest@example.com',
                password='guest123', first_name='Sophie', last_name='Laurent',
                phone='+33 6 12 34 56 78', nationality='French'
            )
            self.stdout.write('  Created test guest: guest@example.com / guest123')

        # Categories
        cats = {}
        for c in CATEGORIES:
            obj, _ = RoomCategory.objects.get_or_create(slug=c['slug'], defaults=c)
            cats[c['slug']] = obj
        self.stdout.write(f'  Created {len(cats)} room categories')

        # Rooms
        count = 0
        for r in ROOMS:
            if not Room.objects.filter(room_number=r['number']).exists():
                room = Room.objects.create(
                    category=cats[r['cat']],
                    name=r['name'],
                    room_number=r['number'],
                    description=r['desc'],
                    short_description=r['short'],
                    price_per_night=r['price'],
                    size_sqm=r['size'],
                    max_guests=r['max'],
                    floor=r['floor'],
                    is_featured=r.get('featured', False),
                    has_sea_view=r.get('sea', False),
                    has_balcony=r.get('balcony', False),
                    has_jacuzzi=r.get('jacuzzi', False),
                    has_fireplace=r.get('fire', False),
                )
                for a in AMENITIES:
                    RoomAmenity.objects.create(room=room, name=a)
                count += 1
        self.stdout.write(f'  Created {count} rooms with amenities')

        # Service categories & services
        sc = {}
        for s in SVC_CATS:
            obj, _ = ServiceCategory.objects.get_or_create(slug=s['slug'], defaults=s)
            sc[s['slug']] = obj
        for s in SERVICES:
            Service.objects.get_or_create(
                name=s['name'],
                defaults={
                    'category': sc[s['cat']],
                    'description': s['desc'],
                    'price': s.get('price'),
                    'duration': s.get('dur', ''),
                    'is_featured': s.get('featured', False),
                }
            )
        self.stdout.write('  Created service categories and services')
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
        self.stdout.write('  Admin: admin@lumiere-hotel.com / admin123')
        self.stdout.write('  Guest: guest@example.com / guest123')
