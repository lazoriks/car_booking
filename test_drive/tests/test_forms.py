from django.test import TestCase
from test_drive.forms import BookingForm, RequestToBuyForm
from datetime import date
from decimal import Decimal


class BookingFormTest(TestCase):

    def test_valid_booking_form(self):
        form_data = {
            'date': date.today(),
            'name': 'John',
            'surname': 'Doe',
            'mobile': '1234567890',
            'email': 'john.doe@example.com',
        }
        form = BookingForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_mobile_in_booking_form(self):
        form_data = {
            'date': date.today(),
            'name': 'John',
            'surname': 'Doe',
            'mobile': '1234',  # Invalid mobile number
            'email': 'john.doe@example.com',
        }
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('mobile', form.errors)

    def test_invalid_email_in_booking_form(self):
        form_data = {
            'date': date.today(),
            'name': 'John',
            'surname': 'Doe',
            'mobile': '1234567890',
            'email': 'john.doe@invalid',  # Invalid email
        }
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_empty_name_or_surname_in_booking_form(self):
        form_data = {
            'date': date.today(),
            'name': '',
            'surname': '',
            'mobile': '1234567890',
            'email': 'john.doe@example.com',
        }
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)  # clean() validation


class RequestToBuyFormTest(TestCase):

    def test_valid_request_to_buy_form(self):
        form_data = {
            'email': 'buyer@example.com',
            'mobile': '1234567890',
            'price': Decimal('15000.00'),
        }
        form = RequestToBuyForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_mobile_in_request_to_buy_form(self):
        form_data = {
            'email': 'buyer@example.com',
            'mobile': '123',  # Invalid mobile number
            'price': Decimal('15000.00'),
        }
        form = RequestToBuyForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('mobile', form.errors)

    def test_invalid_email_in_request_to_buy_form(self):
        form_data = {
            'email': 'buyer@invalid',
            'mobile': '1234567890',
            'price': Decimal('15000.00'),
        }
        form = RequestToBuyForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_negative_price_in_request_to_buy_form(self):
        form_data = {
            'email': 'buyer@example.com',
            'mobile': '1234567890',
            'price': Decimal('-1.00'),  # Negative price
        }
        form = RequestToBuyForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)

    def test_missing_email_and_mobile_in_request_to_buy_form(self):
        form_data = {
            'email': '',
            'mobile': '',
            'price': Decimal('15000.00'),
        }
        form = RequestToBuyForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)  # clean() validation
