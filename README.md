# Lumière Hotel — Luxury Hotel Booking Platform

A complete, production-ready luxury hotel web platform built with Django.

## Features
- 🏨 Full public website (Home, Rooms, Gallery, Services, About, Contact)
- 🔐 User authentication (Register, Login, Profile)
- 📅 Room booking with availability checking & double-booking prevention
- 💳 Simulated payment system (Stripe-ready)
- ⭐ Reviews & ratings
- ❤️ Wishlist / favourites
- 👑 Custom admin dashboard
- 📱 Fully responsive (mobile + tablet + desktop)

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run migrations
python manage.py migrate

# 3. Seed sample data
python manage.py seed_data

# 4. Start server
python manage.py runserver
```

Visit: http://127.0.0.1:8000

## Default Accounts
| Role  | Email | Password |
|-------|-------|----------|
| Admin | admin@lumiere-hotel.com | admin123 |
| Guest | guest@example.com | guest123 |

## Admin Panel
- Custom dashboard: http://127.0.0.1:8000/admin-panel/
- Django admin: http://127.0.0.1:8000/django-admin/

## Project Structure
```
lumiere_hotel/
├── lumiere/          # Project settings & URLs
├── users/            # Auth, profiles
├── rooms/            # Rooms, categories, reviews, favourites
├── bookings/         # Booking logic & availability
├── payments/         # Payment processing (simulated)
├── services/         # Hotel services & gallery
├── templates/        # All HTML templates
├── static/           # CSS, JS
└── media/            # Uploaded images
```

## Tech Stack
- **Backend**: Django 4.2+
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Frontend**: Vanilla JS + CSS Variables
- **Fonts**: Cormorant Garamond (serif) + Jost (sans)
- **Icons**: Font Awesome 6

## Production Deployment
1. Set `DEBUG = False` in settings.py
2. Set a strong `SECRET_KEY`
3. Configure PostgreSQL database
4. Run `python manage.py collectstatic`
5. Use Gunicorn + Nginx
6. Add real Stripe keys for payments
