from django.test import TestCase
from django.contrib.auth.models import User
from test_drive.models import Booking, RequestToBuy
from datetime import date
from decimal import Decimal


class BookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.booking = Booking.objects.create(
            user=self.user,
            date=date(2024, 11, 30),
            name='John',
            surname='Doe',
            mobile='+123456789',
            email='john.doe@example.com'
        )

    def test_booking_creation(self):
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(self.booking.name, 'John')
        self.assertEqual(self.booking.surname, 'Doe')
        self.assertEqual(self.booking.mobile, '+123456789')
        self.assertEqual(self.booking.email, 'john.doe@example.com')

    def test_booking_str(self):
        expected_str = 'John Doe - 2024-11-30'
        self.assertEqual(str(self.booking), expected_str)


class RequestToBuyModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testbuyer', password='testpass')
        self.request_to_buy = RequestToBuy.objects.create(
            user=self.user,
            email='buyer@example.com',
            mobile='+987654321',
            price=Decimal('16300.00')
        )

    def test_request_to_buy_creation(self):
        self.assertEqual(RequestToBuy.objects.count(), 1)
        self.assertEqual(self.request_to_buy.email, 'buyer@example.com')
        self.assertEqual(self.request_to_buy.mobile, '+987654321')
        self.assertEqual(self.request_to_buy.price, Decimal('16300.00'))

    def test_request_to_buy_auto_date(self):
        self.assertEqual(self.request_to_buy.date, date.today())

    def test_request_to_buy_str(self):
        expected_str = f'Request from {self.user.username} on {self.request_to_buy.date}'
        self.assertEqual(str(self.request_to_buy), expected_str)
