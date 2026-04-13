# 🕌 Ma Mangala Travels

A full-stack Django travel booking website focused on **Odisha tourism** — Puri, Chilika Lake & Bhubaneswar.

**Tech Stack:** Django 4.2 • SQLite • HTML/CSS/JS • Golden + Black + Blue theme

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run migrations
python manage.py migrate

# 3. Seed default data (vehicles, settings, sample reviews)
python manage.py seed_data

# 4. Create admin user
python manage.py createsuperuser

# 5. Run the server
python manage.py runserver
```

**Then open:** http://127.0.0.1:8000

---

## 📋 Pages

| Page | URL |
|------|-----|
| Homepage | `/` |
| Destinations | `/destinations/` |
| Vehicles | `/vehicles/` |
| Booking Form | `/booking/` |
| About | `/about/` |
| Contact | `/contact/` |
| Gallery | `/gallery/` |
| **Admin Panel** | **`/admin/`** |

---

## 🛠️ Admin Panel

Go to `/admin/` and log in with your superuser credentials.

**You can:**
- ✅ View and manage all bookings
- ✅ Accept / Reject bookings
- ✅ Set final prices and assign drivers
- ✅ Edit vehicle pricing per km
- ✅ Manage site settings (WhatsApp number, address, tagline)
- ✅ Add/hide customer reviews
- ✅ Upload gallery photos

---

## 💰 Default Pricing

| Vehicle | Per KM | Fixed/Day |
|---------|--------|-----------|
| Hatchback | ₹12 | ₹300 |
| Sedan | ₹16 | ₹400 |
| SUV | ₹22 | ₹500 |

> Formula: `Estimated Price = (Distance × ₹/km) + (Days × ₹/day)`

---

## 📁 Project Structure

```
d:\tisha\
├── manage.py
├── requirements.txt
├── ma_mangala_travels/        ← Django config package
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── travels/                   ← Main app
│   ├── models.py              ← Booking, Vehicle, Review, SiteSettings
│   ├── views.py               ← All page views + AJAX price API
│   ├── admin.py               ← Custom admin
│   ├── forms.py               ← BookingForm
│   ├── urls.py                ← App URL routes
│   └── management/commands/
│       └── seed_data.py       ← Initial data seeder
├── templates/                 ← HTML templates
│   ├── base.html
│   ├── home.html
│   ├── destinations.html
│   ├── vehicles.html
│   ├── booking.html
│   ├── about.html
│   ├── contact.html
│   └── gallery.html
└── static/
    ├── css/style.css          ← Main stylesheet (golden/black/blue)
    ├── js/main.js             ← Animations + price calculator
    └── images/                ← Destination & vehicle images
```
