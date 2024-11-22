from django import forms
from test_drive.models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'name', 'surname', 'mobile', 'email']

class SubscriptionForm(forms.Form):
    email = forms.EmailField(max_length=254, label="Your Email", widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
