"""
Ma Mangala Travels - Forms
Booking form with full validation.
"""

from django import forms
from .models import Booking
import datetime


class BookingForm(forms.ModelForm):
    """
    Main booking form shown on the booking page.
    All fields are validated here before saving to DB.
    """

    travel_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'min': str(datetime.date.today()),  # Prevent past dates
        }),
        label="Travel Date"
    )

    class Meta:
        model = Booking
        fields = [
            'customer_name', 'phone', 'pickup_location',
            'destination', 'travel_date', 'days',
            'car_type', 'notes', 'estimated_price'
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name',
                'id': 'id_customer_name',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91 XXXXXXXXXX',
                'id': 'id_phone',
            }),
            'pickup_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Bhubaneswar Airport',
                'id': 'id_pickup_location',
            }),
            'destination': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_destination',
            }),
            'days': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '30',
                'id': 'id_days',
            }),
            'car_type': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_car_type',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any special requirements?',
                'id': 'id_notes',
            }),
            'estimated_price': forms.HiddenInput(attrs={
                'id': 'id_estimated_price',
            }),
        }
        labels = {
            'customer_name': 'Full Name',
            'phone': 'Phone Number',
            'pickup_location': 'Pickup Location',
            'destination': 'Destination',
            'days': 'Number of Days',
            'car_type': 'Vehicle Type',
            'notes': 'Special Notes (Optional)',
        }

    # Override destination to be a text field (allow custom destinations)
    destination = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. Puri, Chilika Lake, Bhubaneswar',
            'id': 'id_destination',
            'list': 'destination_suggestions',
        }),
        label="Destination"
    )

    def clean_phone(self):
        """Validate phone number format."""
        phone = self.cleaned_data.get('phone', '').strip()
        digits = ''.join(filter(str.isdigit, phone))
        if len(digits) < 10:
            raise forms.ValidationError("Please enter a valid 10-digit phone number.")
        return phone

    def clean_travel_date(self):
        """Ensure travel date is not in the past."""
        date = self.cleaned_data.get('travel_date')
        if date and date < datetime.date.today():
            raise forms.ValidationError("Travel date cannot be in the past.")
        return date

    def clean_days(self):
        """Ensure days is positive."""
        days = self.cleaned_data.get('days')
        if days and days < 1:
            raise forms.ValidationError("Number of days must be at least 1.")
        return days
