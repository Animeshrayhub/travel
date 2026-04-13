"""
Ma Mangala Travels - URL Configuration
All page routes for the travels app.
"""

from django.urls import path
from . import views

app_name = 'travels'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('destinations/', views.destinations, name='destinations'),
    path('vehicles/', views.vehicles, name='vehicles'),
    path('booking/', views.booking, name='booking'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('gallery/', views.gallery, name='gallery'),

    # AJAX endpoints
    path('api/price-estimate/', views.price_estimate_api, name='price_estimate_api'),
    path('api/booking-success/', views.booking_success, name='booking_success'),
]
