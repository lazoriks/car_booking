from django import forms


# BookingForm lives in test_drive.forms — removed duplicate that imported across apps
class SubscriptionForm(forms.Form):
    email = forms.EmailField(max_length=254, label="Your Email", widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
