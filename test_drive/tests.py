# car_booking/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Booking, RequestToBuy
from .forms import BookingForm, RequestToBuyForm


# test models
class BookingModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.booking = Booking.objects.create(
            user=self.user,
            date='2024-11-07',
            name='John',
            surname='Doe',
            mobile='123456789',
            email='john.doe@example.com'
        )
    
    def test_booking_creation(self):
        self.assertEqual(self.booking.name, 'John')
        self.assertEqual(self.booking.surname, 'Doe')
        self.assertEqual(self.booking.mobile, '123456789')
        self.assertEqual(self.booking.email, 'john.doe@example.com')

class RequestToBuyModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.request = RequestToBuy.objects.create(
            user=self.user,
            email='john.doe@example.com',
            mobile='123456789',
            price=12345.67
        )
    
    def test_request_creation(self):
        self.assertEqual(self.request.email, 'john.doe@example.com')
        self.assertEqual(self.request.mobile, '123456789')
        self.assertEqual(self.request.price, 12345.67)

# test views
class BookingViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('booking_view')

    def test_booking_page_accessible_when_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_booking_page_redirect_when_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, '/login/?next=' + self.url)

# test forms
class BookingFormTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_booking_form_valid(self):
        form_data = {
            'user': self.user,
            'date': '2024-11-07',
            'name': 'John',
            'surname': 'Doe',
            'mobile': '123456789',
            'email': 'john.doe@example.com'
        }
        form = BookingForm(data=form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_booking_form_invalid(self):
        form_data = {
            'user': self.user,
            'name': 'John',
            'surname': 'Doe',
            'mobile': '123456789',
        }
        form = BookingForm(data=form_data)
        print(form.errors)
        self.assertFalse(form.is_valid())


class RequestToBuyFormTestCase(TestCase):

    def setUp(self):
        # create user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_request_to_buy_form_valid(self):
        # corect
        form_data = {
            'email': 'john.doe@example.com',
            'mobile': '123456789012345',  
            'price': 123.45,  
        }
        form = RequestToBuyForm(data=form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_request_to_buy_form_invalid_mobile(self):
        # incorect mobile
        form_data = {
            'email': 'john.doe@example.com',
            'mobile': '1234567890',  
            'price': 123.45,
        }
        form = RequestToBuyForm(data=form_data)
        print(form.errors)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['mobile'], ['Mobile number must be 15 characters.'])

    def test_request_to_buy_form_invalid_price(self):
        # incorect price
        form_data = {
            'email': 'john.doe@example.com',
            'mobile': '123456789012345',
            'price': -10.00,  
        }
        form = RequestToBuyForm(data=form_data)
        print(form.errors)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['price'], ['Price must be greater than zero.'])

    def test_request_to_buy_form_missing_fields(self):
        # test empty
        form_data = {
            'email': '',  
            'mobile': '123456789012345',
            'price': 123.45,
        }
        form = RequestToBuyForm(data=form_data)
        print(form.errors)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['This field is required.'])
