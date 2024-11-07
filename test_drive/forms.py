from django import forms
from .models import Booking, RequestToBuy
import re


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'name', 'surname', 'mobile', 'email']

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        # only numbers, lens from 10 to 15
        if not re.match(r'^\d{10,15}$', mobile):
            raise forms.ValidationError(f'''
Mobile number must be 15 characters.
''')
        return mobile

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # formate email
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            raise forms.ValidationError('Error formate email.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        surname = cleaned_data.get('surname')

        # empty
        if not name or not surname:
            raise forms.ValidationError('Name and Surname couldnt be empty.')

        return cleaned_data


class RequestToBuyForm(forms.ModelForm):
    class Meta:
        model = RequestToBuy
        fields = ['email', 'mobile', 'price']

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        # only numbers, lens from 10 to 15
        if not re.match(r'^\d{10,15}$', mobile):
            raise forms.ValidationError(f'''
Number mobile must be only numbers and from 10 to 15.
''')
        return mobile

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # formate email
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            raise forms.ValidationError('Error formate email.')
        return email

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError('Price must be greater than zero.')
        return price

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        mobile = cleaned_data.get('mobile')

        # is empty mobile and email
        if not email and not mobile:
            raise forms.ValidationError('Must be input email or mobile')

        return cleaned_data
