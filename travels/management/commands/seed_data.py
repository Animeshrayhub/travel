"""
Management command: seed_data
Populates the database with initial vehicles, site settings, and sample reviews.

Usage:
    python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from travels.models import Vehicle, CustomerReview, SiteSettings


class Command(BaseCommand):
    help = 'Seeds the database with default vehicles, settings, and sample reviews'

    def handle(self, *args, **kwargs):
        self.seed_settings()
        self.seed_vehicles()
        self.seed_reviews()
        self.stdout.write(self.style.SUCCESS('✅ Database seeded successfully!'))

    def seed_settings(self):
        """Create default site settings (singleton)."""
        settings, created = SiteSettings.objects.get_or_create(pk=1)
        if created:
            settings.whatsapp_number = '+91 9876543210'
            settings.address = 'Ma Mangala Travels, Near Sea Beach Road, Puri, Odisha - 752001'
            settings.email = 'info@mamangalatravels.com'
            settings.tagline = 'Discover the Soul of Odisha'
            settings.save()
            self.stdout.write('  ✓ Site settings created')
        else:
            self.stdout.write('  · Site settings already exist (skipped)')

    def seed_vehicles(self):
        """Create the 3 default vehicle types."""
        vehicles_data = [
            {
                'name': 'Economy Hatchback',
                'car_type': 'hatchback',
                'price_per_km': 12,
                'fixed_daily_charge': 300,
                'capacity': 4,
                'description': 'Compact and fuel-efficient. Perfect for 2–4 passengers on city and short trips to Puri or Bhubaneswar.',
                'is_active': True,
            },
            {
                'name': 'Comfort Sedan',
                'car_type': 'sedan',
                'price_per_km': 16,
                'fixed_daily_charge': 400,
                'capacity': 5,
                'description': 'Spacious and comfortable with ample legroom. Ideal for family trips to Puri, Chilika Lake, or full temple circuits.',
                'is_active': True,
            },
            {
                'name': 'Premium SUV',
                'car_type': 'suv',
                'price_per_km': 22,
                'fixed_daily_charge': 500,
                'capacity': 7,
                'description': 'Ultimate group comfort for up to 7 passengers. Handles any terrain — perfect for the full Odisha Grand Tour.',
                'is_active': True,
            },
        ]

        for data in vehicles_data:
            vehicle, created = Vehicle.objects.get_or_create(
                car_type=data['car_type'],
                defaults=data
            )
            status = 'created' if created else 'already exists (skipped)'
            self.stdout.write(f'  ✓ {data["name"]}: {status}')

    def seed_reviews(self):
        """Add sample customer reviews."""
        if CustomerReview.objects.exists():
            self.stdout.write('  · Reviews already exist (skipped)')
            return

        reviews_data = [
            {
                'customer_name': 'Rahul Sharma',
                'from_city': 'Kolkata',
                'rating': 5,
                'comment': 'Ma Mangala Travels made our Puri trip unforgettable! The driver was punctual, the car was clean, and the service was excellent. Highly recommended!',
                'is_visible': True,
            },
            {
                'customer_name': 'Priya Patel',
                'from_city': 'Hyderabad',
                'rating': 5,
                'comment': 'Booked a sedan for 3 days across Odisha. The itinerary was perfect and the team was very responsive on WhatsApp. Will definitely book again!',
                'is_visible': True,
            },
            {
                'customer_name': 'Amit Kumar',
                'from_city': 'Delhi',
                'rating': 5,
                'comment': 'The Chilika Lake boat safari arranged through Ma Mangala was the highlight of our entire trip. Very authentic and well-organized experience.',
                'is_visible': True,
            },
            {
                'customer_name': 'Sunita Das',
                'from_city': 'Mumbai',
                'rating': 5,
                'comment': 'As a solo traveler, I felt completely safe with their driver. Bhubaneswar temple tour was beautifully planned. Lingaraj Temple was breathtaking!',
                'is_visible': True,
            },
            {
                'customer_name': 'Vikram Singh',
                'from_city': 'Bengaluru',
                'rating': 4,
                'comment': 'Great service at competitive prices. Our family trip to Puri and Konark was stress-free and memorable. The SUV was very spacious and comfortable.',
                'is_visible': True,
            },
            {
                'customer_name': 'Meera Reddy',
                'from_city': 'Chennai',
                'rating': 5,
                'comment': 'Friendly staff, clean car, and perfect local knowledge. Our driver took us to a hidden beach in Puri that was absolutely stunning!',
                'is_visible': True,
            },
        ]

        for review_data in reviews_data:
            CustomerReview.objects.create(**review_data)

        self.stdout.write(f'  ✓ {len(reviews_data)} sample reviews added')
