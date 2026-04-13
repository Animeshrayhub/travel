"""
Ma Mangala Travels - Views
All page view functions and AJAX endpoints.
"""

import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import Vehicle, CustomerReview, SiteSettings, GalleryPhoto, Booking
from .forms import BookingForm


# ─── Pricing Table (used in both views and JS) ───
# These rates match the Vehicle DB records seeded by management command
PRICE_TABLE = {
    'hatchback': {'per_km': 12, 'per_day': 300},
    'sedan':     {'per_km': 16, 'per_day': 400},
    'suv':       {'per_km': 22, 'per_day': 500},
}

# Approximate distances from Bhubaneswar (km) — used for estimate
DESTINATION_DISTANCES = {
    'puri': 60,
    'chilika lake': 110,
    'bhubaneswar': 10,
    'konark': 65,
}


# ─────────────────────────────────────────────
#  Helper
# ─────────────────────────────────────────────
def get_site_settings():
    """Return SiteSettings singleton, creating defaults if needed."""
    return SiteSettings.get_settings()


# ─────────────────────────────────────────────
#  Homepage
# ─────────────────────────────────────────────
def home(request):
    vehicles = Vehicle.objects.filter(is_active=True)[:3]
    reviews = CustomerReview.objects.filter(is_visible=True)[:6]
    settings = get_site_settings()

    # Static fallback reviews shown when DB has none
    default_reviews = [
        {'name': 'Rahul Sharma', 'city': 'Kolkata', 'text': 'Ma Mangala Travels made our Puri trip unforgettable. The driver was punctual, the car was clean, and the service was excellent!'},
        {'name': 'Priya Patel', 'city': 'Hyderabad', 'text': 'Booked a sedan for 3 days across Odisha. The itinerary was perfect and the team was very responsive on WhatsApp. Will book again!'},
        {'name': 'Amit Kumar', 'city': 'Delhi', 'text': 'The Chilika Lake boat safari arranged through Ma Mangala was the highlight of our trip. Very authentic and well-organized.'},
        {'name': 'Sunita Das', 'city': 'Mumbai', 'text': 'As a solo traveler, I felt completely safe with their driver. Bhubaneswar temples tour was beautifully planned. Highly recommend!'},
        {'name': 'Vikram Singh', 'city': 'Bangalore', 'text': 'Great service at great prices! Our family trip to Puri and Konark was stress-free and memorable. The SUV was very comfortable.'},
        {'name': 'Meera Reddy', 'city': 'Chennai', 'text': 'Friendly staff, clean car, and perfect local knowledge. The driver took us to a hidden beach in Puri that was absolutely stunning!'},
    ]

    context = {
        'page_title': 'Ma Mangala Travels — Discover Odisha',
        'vehicles': vehicles,
        'reviews': reviews,
        'default_reviews': default_reviews,
        'settings': settings,
        'whatsapp_link': f"https://wa.me/{settings.whatsapp_number.replace('+', '').replace(' ', '')}",
    }
    return render(request, 'home.html', context)


# ─────────────────────────────────────────────
#  Destinations
# ─────────────────────────────────────────────
def destinations(request):
    settings = get_site_settings()
    destinations_data = [
        {
            'name': 'Puri',
            'slug': 'puri',
            'tagline': 'The Sacred Beach City',
            'description': (
                'Puri is one of the four sacred dhams of Hinduism, famous for the '
                'magnificent Jagannath Temple and its beautiful golden beach. '
                'Experience the divine blend of spirituality and serenity.'
            ),
            'image': 'images/puri_beach.png',
            'distance': '60 km from Bhubaneswar',
            'best_time': 'October – March',
            'highlights': ['Jagannath Temple', 'Puri Beach', 'Rath Yatra Festival', 'Chilika (30 km)'],
            'itinerary': [
                {'day': 'Day 1', 'plan': 'Arrive Puri, visit Jagannath Temple, evening at beach'},
                {'day': 'Day 2', 'plan': 'Sunrise at beach, Konark Sun Temple (35 km), return'},
            ]
        },
        {
            'name': 'Chilika Lake',
            'slug': 'chilika',
            'tagline': "Asia's Largest Brackish Water Lake",
            'description': (
                'Chilika Lake is a biodiversity hotspot and home to over 160 species of '
                'birds, including rare flamingos. Take a boat ride to Kalijai Island and '
                'spot Irrawaddy dolphins in their natural habitat.'
            ),
            'image': 'images/chilika_lake.png',
            'distance': '110 km from Bhubaneswar',
            'best_time': 'November – February (migratory birds)',
            'highlights': ['Dolphin Sighting', 'Kalijai Island', 'Bird Watching', 'Boat Safari'],
            'itinerary': [
                {'day': 'Day 1', 'plan': 'Reach Satapada, boat ride for dolphin spotting, sunset cruise'},
                {'day': 'Day 2', 'plan': 'Visit Kalijai Island, birdwatching at Mangalajodi, return'},
            ]
        },
        {
            'name': 'Bhubaneswar',
            'slug': 'bhubaneswar',
            'tagline': 'The Temple City of India',
            'description': (
                'Bhubaneswar, the capital of Odisha, is dotted with over 700 ancient temples. '
                'The Lingaraj Temple, Mukteswar Temple, and the world-class Odisha State Museum '
                'make this a cultural treasure trove.'
            ),
            'image': 'images/bhubaneswar_temple.png',
            'distance': 'City Base',
            'best_time': 'October – March',
            'highlights': ['Lingaraj Temple', 'Mukteswar Temple', 'Udayagiri Caves', 'Ekamra Kanan'],
            'itinerary': [
                {'day': 'Day 1', 'plan': 'Lingaraj Temple, Mukteswar Temple, State Museum'},
                {'day': 'Day 2', 'plan': 'Udayagiri & Khandagiri Caves, ISKCON Temple, Ekamra Kanan'},
            ]
        },
    ]

    context = {
        'page_title': 'Destinations — Ma Mangala Travels',
        'destinations_data': destinations_data,
        'settings': settings,
    }
    return render(request, 'destinations.html', context)


# ─────────────────────────────────────────────
#  Vehicles
# ─────────────────────────────────────────────
def vehicles(request):
    vehicles_list = Vehicle.objects.filter(is_active=True)
    settings = get_site_settings()

    static_vehicles = [
        {'type': 'hatchback', 'type_display': 'Hatchback', 'name': 'Economy Ride', 'desc': 'Compact & fuel-efficient. Perfect for 2–4 passengers on city and short trips.', 'per_km': 12, 'per_day': 300, 'seats': 4},
        {'type': 'sedan', 'type_display': 'Sedan', 'name': 'Comfort Ride', 'desc': 'Spacious and comfortable. Great for families on longer trips to Puri or Chilika.', 'per_km': 16, 'per_day': 400, 'seats': 5},
        {'type': 'suv', 'type_display': 'SUV', 'name': 'Premium Ride', 'desc': 'Ultimate comfort for groups or premium travelers. Handles any terrain with ease.', 'per_km': 22, 'per_day': 500, 'seats': 7},
    ]

    context = {
        'page_title': 'Our Vehicles — Ma Mangala Travels',
        'vehicles': vehicles_list,
        'static_vehicles': static_vehicles,
        'settings': settings,
    }
    return render(request, 'vehicles.html', context)


# ─────────────────────────────────────────────
#  Booking Page
# ─────────────────────────────────────────────
def booking(request):
    settings = get_site_settings()

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking_obj = form.save()
            messages.success(
                request,
                f"✅ Booking submitted successfully! We'll contact you at {booking_obj.phone} soon."
            )
            return redirect('travels:booking')
        else:
            messages.error(request, "❌ Please correct the errors below.")
    else:
        form = BookingForm()

    # Pass pricing data to template (for JS calculator)
    price_data = json.dumps(PRICE_TABLE)

    promises = [
        {'icon': '✅', 'title': 'Instant Estimate', 'desc': 'See your price before booking. No surprises.'},
        {'icon': '📞', 'title': 'Quick Confirmation', 'desc': 'We confirm within 2 hours via WhatsApp or call.'},
        {'icon': '🛡️', 'title': 'Safe Journeys', 'desc': 'Verified drivers, insured vehicles, GPS tracked.'},
        {'icon': '💰', 'title': 'Best Prices', 'desc': 'Competitive fares with no hidden charges.'},
    ]

    context = {
        'page_title': 'Book Your Ride — Ma Mangala Travels',
        'form': form,
        'price_data': price_data,
        'settings': settings,
        'destinations': list(DESTINATION_DISTANCES.keys()),
        'promises': promises,
    }
    return render(request, 'booking.html', context)


# ─────────────────────────────────────────────
#  About Page
# ─────────────────────────────────────────────
def about(request):
    settings = get_site_settings()
    milestones = [
        {'icon': '🚗', 'year': '2017', 'title': 'Founded', 'desc': 'Started with 2 vehicles and a passion for Odisha tourism.'},
        {'icon': '🌟', 'year': '2019', 'title': '100 Trips Done', 'desc': 'Reached our first 100 successful bookings across Puri & Chilika.'},
        {'icon': '🚙', 'year': '2021', 'title': 'Fleet Expanded', 'desc': 'Added SUVs and sedans to cater to all traveler needs.'},
        {'icon': '🏆', 'year': '2024', 'title': '500+ Travelers', 'desc': 'Trusted by over 500 happy travelers. Growing every month!'},
    ]

    context = {
        'page_title': 'About Us — Ma Mangala Travels',
        'settings': settings,
        'milestones': milestones,
    }
    return render(request, 'about.html', context)


# ─────────────────────────────────────────────
#  Contact Page
# ─────────────────────────────────────────────
def contact(request):
    settings = get_site_settings()
    wa_number = settings.whatsapp_number.replace('+', '').replace(' ', '')

    faqs = [
        {'q': 'How do I book a ride?', 'a': 'Fill out the booking form on our website. Our team will contact you within 2 hours to confirm.'},
        {'q': 'Is advance payment required?', 'a': 'No! We do not require any advance payment. Pay only after your trip is confirmed by our admin.'},
        {'q': 'Can I customize my itinerary?', 'a': 'Absolutely! Contact us on WhatsApp and we will design a custom itinerary just for you.'},
        {'q': 'What is included in the price?', 'a': 'Our base price includes the vehicle, fuel, and driver. Entry tickets to temples or boat rides are not included unless mentioned.'},
        {'q': 'Do you operate 24/7?', 'a': 'We are available from 6 AM to 10 PM IST. For early morning departures, please book a day in advance.'},
        {'q': 'Can I get a receipt after my trip?', 'a': 'Yes, we provide a digital receipt via WhatsApp after your journey is completed.'},
    ]

    context = {
        'page_title': 'Contact Us — Ma Mangala Travels',
        'settings': settings,
        'whatsapp_link': f"https://wa.me/{wa_number}",
        'faqs': faqs,
    }
    return render(request, 'contact.html', context)


# ─────────────────────────────────────────────
#  Gallery Page
# ─────────────────────────────────────────────
def gallery(request):
    photos = GalleryPhoto.objects.filter(is_visible=True)
    settings = get_site_settings()
    context = {
        'page_title': 'Gallery — Ma Mangala Travels',
        'photos': photos,
        'settings': settings,
    }
    return render(request, 'gallery.html', context)


# ─────────────────────────────────────────────
#  AJAX: Live Price Estimate
# ─────────────────────────────────────────────
def price_estimate_api(request):
    """
    AJAX endpoint: calculates estimated trip price.
    GET params: car_type, days, distance (optional)
    Returns JSON: { estimated_price, breakdown }
    """
    car_type = request.GET.get('car_type', 'hatchback').lower()
    try:
        days = max(1, int(request.GET.get('days', 1)))
    except ValueError:
        days = 1

    dest = request.GET.get('destination', '').lower().strip()
    distance = DESTINATION_DISTANCES.get(dest, 60)  # default 60 km

    rates = PRICE_TABLE.get(car_type, PRICE_TABLE['hatchback'])
    distance_charge = distance * rates['per_km']
    day_charge = days * rates['per_day']
    total = distance_charge + day_charge

    return JsonResponse({
        'estimated_price': total,
        'breakdown': {
            'distance_km': distance,
            'per_km_rate': rates['per_km'],
            'distance_charge': distance_charge,
            'days': days,
            'per_day_charge': rates['per_day'],
            'day_charge': day_charge,
            'total': total,
        }
    })


# ─────────────────────────────────────────────
#  AJAX: Booking Success (unused – uses redirect instead)
# ─────────────────────────────────────────────
def booking_success(request):
    return JsonResponse({'status': 'ok', 'message': 'Booking submitted!'})
