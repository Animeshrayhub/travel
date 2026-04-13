"""
Ma Mangala Travels - Database Models
Defines all data structures for the travel booking system.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# ─────────────────────────────────────────────
#  Vehicle Model
#  Stores car types with pricing & capacity info
# ─────────────────────────────────────────────
class Vehicle(models.Model):
    CAR_TYPE_CHOICES = [
        ('hatchback', 'Hatchback'),
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
    ]

    name = models.CharField(max_length=100, help_text="e.g. Maruti Swift")
    car_type = models.CharField(max_length=20, choices=CAR_TYPE_CHOICES)
    price_per_km = models.DecimalField(max_digits=8, decimal_places=2, help_text="Rate in ₹ per km")
    fixed_daily_charge = models.DecimalField(max_digits=8, decimal_places=2, help_text="Fixed charge per day in ₹")
    capacity = models.PositiveIntegerField(help_text="Number of passengers")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['car_type']
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"

    def __str__(self):
        return f"{self.name} ({self.get_car_type_display()})"


# ─────────────────────────────────────────────
#  Booking Model
#  Core booking request from customers
# ─────────────────────────────────────────────
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    CAR_TYPE_CHOICES = [
        ('hatchback', 'Hatchback'),
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
    ]

    # Customer info
    customer_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)

    # Trip details
    pickup_location = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    travel_date = models.DateField()
    days = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    car_type = models.CharField(max_length=20, choices=CAR_TYPE_CHOICES)
    notes = models.TextField(blank=True, help_text="Any special instructions")

    # Pricing
    estimated_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        help_text="Auto-calculated estimate shown to customer"
    )
    final_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text="Admin sets final confirmed price"
    )

    # Admin management
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    assigned_driver = models.CharField(
        max_length=150, blank=True,
        help_text="Driver name assigned by admin"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"

    def __str__(self):
        return f"{self.customer_name} → {self.destination} ({self.travel_date})"

    def get_status_color(self):
        """Returns Bootstrap badge color based on status."""
        colors = {'pending': 'warning', 'accepted': 'success', 'rejected': 'danger'}
        return colors.get(self.status, 'secondary')


# ─────────────────────────────────────────────
#  CustomerReview Model
#  Testimonials shown on homepage
# ─────────────────────────────────────────────
class CustomerReview(models.Model):
    customer_name = models.CharField(max_length=150)
    from_city = models.CharField(max_length=100, blank=True, help_text="e.g. Kolkata")
    rating = models.PositiveIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    is_visible = models.BooleanField(default=True, help_text="Show on website")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Customer Review"
        verbose_name_plural = "Customer Reviews"

    def __str__(self):
        return f"{self.customer_name} - {self.rating}★"


# ─────────────────────────────────────────────
#  SiteSettings Model
#  Singleton model for admin-editable site config
# ─────────────────────────────────────────────
class SiteSettings(models.Model):
    whatsapp_number = models.CharField(
        max_length=20, default="+91 XXXXXXXXXX",
        help_text="WhatsApp number displayed on contact page (with country code)"
    )
    address = models.TextField(
        default="Ma Mangala Travels, Puri, Odisha, India",
        help_text="Office address"
    )
    email = models.EmailField(blank=True, default="info@mamangalatravels.com")
    tagline = models.CharField(
        max_length=200,
        default="Discover the Soul of Odisha",
        help_text="Hero section tagline"
    )
    about_text = models.TextField(
        default=(
            "Ma Mangala Travels is a trusted local travel company based in Odisha, "
            "dedicated to providing authentic and memorable travel experiences across "
            "Puri, Chilika Lake, and Bhubaneswar. We are committed to safe, comfortable, "
            "and affordable journeys."
        )
    )

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

    def save(self, *args, **kwargs):
        """Enforce singleton — only one settings record allowed."""
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        """Always returns the settings object, creating defaults if needed."""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


# ─────────────────────────────────────────────
#  GalleryPhoto Model
# ─────────────────────────────────────────────
class GalleryPhoto(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='gallery/')
    location = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', '-id']
        verbose_name = "Gallery Photo"
        verbose_name_plural = "Gallery Photos"

    def __str__(self):
        return self.title
