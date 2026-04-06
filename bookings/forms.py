from django import forms
from .models import Booking
from rooms.models import Room
from django.core.exceptions import ValidationError
from datetime import date

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in', 'check_out', 'guests', 'special_requests']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
            'special_requests': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, room=None, *args, **kwargs):
        self.room = room
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        check_in = cleaned.get('check_in')
        check_out = cleaned.get('check_out')
        guests = cleaned.get('guests')

        if check_in and check_out:
            if check_in < date.today():
                raise ValidationError("Check-in date cannot be in the past.")
            if check_out <= check_in:
                raise ValidationError("Check-out must be after check-in.")
            if self.room:
                if guests and guests > self.room.max_guests:
                    raise ValidationError(f"This room supports max {self.room.max_guests} guests.")
                conflict = Booking.objects.filter(
                    room=self.room,
                    status__in=['pending', 'confirmed', 'checked_in'],
                    check_in__lt=check_out,
                    check_out__gt=check_in,
                )
                if self.instance.pk:
                    conflict = conflict.exclude(pk=self.instance.pk)
                if conflict.exists():
                    raise ValidationError("This room is not available for the selected dates.")
        return cleaned

class SearchForm(forms.Form):
    check_in = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    check_out = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    guests = forms.IntegerField(min_value=1, max_value=10, required=False, initial=1)
    min_price = forms.DecimalField(required=False, min_value=0)
    max_price = forms.DecimalField(required=False, min_value=0)
    category = forms.CharField(required=False)
    sea_view = forms.BooleanField(required=False)
    has_balcony = forms.BooleanField(required=False)
    has_jacuzzi = forms.BooleanField(required=False)
