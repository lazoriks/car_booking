from django import forms
from .models import Booking, RequestToBuy
import re


class BookingForm(forms.ModelForm):
    date = forms.DateField(
        label="Preferred Date",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    name = forms.CharField(
        label="First Name",
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your first name'})
    )
    surname = forms.CharField(
        label="Last Name",
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your last name'})
    )
    mobile = forms.CharField(
        label="Mobile Number",
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your mobile number'})
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )

    class Meta:
        model = Booking
        fields = ['date', 'name', 'surname', 'mobile', 'email']

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if not re.match(r'^\d{10,15}$', mobile):
            raise forms.ValidationError(
                "Mobile number must be between 10 and 15 digits."
            )
        return mobile

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            raise forms.ValidationError("Invalid email format.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        surname = cleaned_data.get('surname')

        if not name or not surname:
            raise forms.ValidationError("Name and Surname cannot be empty.")
        return cleaned_data


class RequestToBuyForm(forms.ModelForm):
    email = forms.EmailField(
        label="Email Address",
        required=False,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )
    mobile = forms.CharField(
        label="Mobile Number",
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your mobile number'})
    )
    price = forms.DecimalField(
        label="Proposed Price",
        min_value=0.01,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter your proposed price'})
    )

    class Meta:
        model = RequestToBuy
        fields = ['email', 'mobile', 'price']

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if mobile and not re.match(r'^\d{10,15}$', mobile):
            raise forms.ValidationError(
                "Mobile number must be between 10 and 15 digits and contain only numbers."
            )
        return mobile

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            raise forms.ValidationError("Invalid email format.")
        return email

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        mobile = cleaned_data.get('mobile')

        if not email and not mobile:
            raise forms.ValidationError("At least one of email or mobile must be provided.")
        return cleaned_data
