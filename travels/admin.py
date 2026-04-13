"""
Ma Mangala Travels - Admin Panel Configuration
Custom admin views for managing bookings, vehicles, reviews, and site settings.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Booking, Vehicle, CustomerReview, SiteSettings, GalleryPhoto


# ─────────────────────────────────────────────
#  Booking Admin
# ─────────────────────────────────────────────
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'customer_name', 'phone', 'destination',
        'travel_date', 'days', 'car_type_badge',
        'status_badge', 'estimated_price', 'final_price',
        'assigned_driver', 'created_at'
    ]
    list_filter = ['status', 'car_type', 'travel_date']
    search_fields = ['customer_name', 'phone', 'destination', 'pickup_location', 'assigned_driver']
    # Note: list_editable removed — use the detail view to edit status/final_price/driver
    # (list_editable fields must match list_display raw field names, not callables)
    readonly_fields = ['estimated_price', 'created_at', 'updated_at']
    ordering = ['-created_at']
    date_hierarchy = 'travel_date'

    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'phone')
        }),
        ('Trip Details', {
            'fields': ('pickup_location', 'destination', 'travel_date', 'days', 'car_type', 'notes')
        }),
        ('Pricing', {
            'fields': ('estimated_price', 'final_price'),
            'description': 'Estimated price is auto-calculated. Set final price after acceptance.'
        }),
        ('Admin Management', {
            'fields': ('status', 'assigned_driver'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def status_badge(self, obj):
        """Show colored status badge in admin list."""
        colors = {
            'pending': '#f59e0b',
            'accepted': '#10b981',
            'rejected': '#ef4444',
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background:{};color:white;padding:3px 10px;border-radius:12px;font-size:12px;font-weight:600;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def car_type_badge(self, obj):
        """Show car type badge."""
        icons = {'hatchback': '🚗', 'sedan': '🚙', 'suv': '🚕'}
        icon = icons.get(obj.car_type, '🚘')
        return format_html('{} {}', icon, obj.get_car_type_display())
    car_type_badge.short_description = 'Car Type'


# ─────────────────────────────────────────────
#  Vehicle Admin
# ─────────────────────────────────────────────
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'car_type', 'price_per_km',
        'fixed_daily_charge', 'capacity', 'is_active'
    ]
    list_editable = ['price_per_km', 'fixed_daily_charge', 'is_active']
    list_filter = ['car_type', 'is_active']
    search_fields = ['name']

    fieldsets = (
        ('Vehicle Info', {
            'fields': ('name', 'car_type', 'description', 'image', 'is_active')
        }),
        ('Capacity & Pricing', {
            'fields': ('capacity', 'price_per_km', 'fixed_daily_charge')
        }),
    )


# ─────────────────────────────────────────────
#  Customer Review Admin
# ─────────────────────────────────────────────
@admin.register(CustomerReview)
class CustomerReviewAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'from_city', 'rating_stars', 'is_visible', 'created_at']
    list_editable = ['is_visible']
    list_filter = ['rating', 'is_visible']
    search_fields = ['customer_name', 'from_city', 'comment']

    def rating_stars(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html(
            '<span style="color:#D4AF37;font-size:16px;">{}</span>', stars
        )
    rating_stars.short_description = 'Rating'


# ─────────────────────────────────────────────
#  Site Settings Admin (Singleton)
# ─────────────────────────────────────────────
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Only one instance allowed — singleton pattern."""

    def has_add_permission(self, request):
        """Prevent creating more than one settings record."""
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    fieldsets = (
        ('Contact Information', {
            'fields': ('whatsapp_number', 'email', 'address'),
        }),
        ('Website Content', {
            'fields': ('tagline', 'about_text'),
        }),
    )


# ─────────────────────────────────────────────
#  Gallery Photo Admin
# ─────────────────────────────────────────────
@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'order', 'is_visible']
    list_editable = ['order', 'is_visible']
    search_fields = ['title', 'location']


# ─────────────────────────────────────────────
#  Admin Site Branding
# ─────────────────────────────────────────────
admin.site.site_header = "🕌 Ma Mangala Travels Admin"
admin.site.site_title = "Ma Mangala Travels"
admin.site.index_title = "Travel Booking Management"
