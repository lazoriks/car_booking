from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from test_drive.models import Booking, RequestToBuy
from datetime import date
from decimal import Decimal


class BookingAndRequestViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_create_booking_and_request_post_valid(self):
        booking_data = {
            'date': date.today(),
            'name': 'John',
            'surname': 'Doe',
            'mobile': '1234567890',
            'email': 'john.doe@example.com',
        }
        request_data = {
            'email': 'john.doe@example.com',
            'mobile': '1234567890',
            'price': Decimal('15000.00'),
        }
        # Fixed: URL name was 'create_booking_and_request' but urls.py registers it as 'booking_view'
        response = self.client.post(reverse('booking_view'), data={**booking_data, **request_data})

        self.assertRedirects(response, reverse('index'))
        self.assertTrue(Booking.objects.filter(user=self.user).exists())
        self.assertTrue(RequestToBuy.objects.filter(user=self.user).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Your booking and request to buy have been submitted.")

    def test_create_booking_and_request_post_invalid(self):
        invalid_data = {
            'date': '',
            'name': '',
            'surname': '',
            'mobile': '123',
            'email': 'invalidemail',
        }
        # Fixed: URL name corrected (was 'create_booking_and_request', registered as 'booking_view')
        response = self.client.post(reverse('booking_view'), data=invalid_data)

        # Fixed: error messages updated to match the actual messages in test_drive/forms.py
        self.assertFormError(response, 'booking_form', 'mobile', 'Mobile number must be between 10 and 15 digits.')
        self.assertFormError(response, 'booking_form', 'email', 'Invalid email format.')
        self.assertFormError(response, 'booking_form', '__all__', 'Name and Surname cannot be empty.')
        self.assertFormError(response, 'request_form', 'mobile', 'Mobile number must be between 10 and 15 digits and contain only numbers.')

    def test_create_booking_and_request_not_logged_in(self):
        self.client.logout()
        # Fixed: URL name corrected from 'create_booking_and_request' to 'booking_view'
        response = self.client.get(reverse('booking_view'))
        self.assertRedirects(response, f'/accounts/login/?next={reverse("booking_view")}')


class ReportViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.booking = Booking.objects.create(
            user=self.user,
            date=date.today(),
            name="John",
            surname="Doe",
            mobile="1234567890",
            email="john.doe@example.com"
        )
        self.request_to_buy = RequestToBuy.objects.create(
            user=self.user,
            email="john.doe@example.com",
            mobile="1234567890",
            price=Decimal('15000.00')
        )

    def test_report_view(self):
        # Fixed: URL name corrected from 'report_view' to 'report' (as registered in test_drive/urls.py)
        response = self.client.get(reverse('report'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.booking.name)
        self.assertContains(response, self.request_to_buy.email)
        self.assertTemplateUsed(response, 'booking/report.html')


class LoginOrRegisterViewTest(TestCase):

    def test_login_and_register_view(self):
        response = self.client.get(reverse('login_or_register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_valid_user(self):
        user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        response = self.client.post(reverse('login_or_register'), {'username': 'testuser', 'password': 'testpassword', 'login': 'Login'})
        # Fixed: URL name corrected from 'booking' (unregistered) to 'booking_view'
        self.assertRedirects(response, reverse('booking_view'))

    def test_register_new_user(self):
        response = self.client.post(reverse('login_or_register'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'register': 'Register'
        })
        # Fixed: URL name corrected from 'booking' (unregistered) to 'booking_view'
        self.assertRedirects(response, reverse('booking_view'))
        self.assertTrue(get_user_model().objects.filter(username='newuser').exists())

    def test_invalid_login(self):
        response = self.client.post(reverse('login_or_register'), {'username': 'invaliduser', 'password': 'wrongpassword', 'login': 'Login'})
        # Fixed: form context var is 'login_form' not 'form'; invalid-credential
        # error is a non-field error (None), not on the 'username' field.
        self.assertFormError(
            response, 'login_form', None,
            'Please enter a correct username and password. Note that both fields may be case-sensitive.'
        )

    def test_invalid_registration(self):
        response = self.client.post(reverse('login_or_register'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'wrongpassword123',
            'register': 'Register'
        })
        # Fixed: form context var is 'register_form' not 'form';
        # Django uses a Unicode right-apostrophe (U+2019) in this message.
        self.assertFormError(response, 'register_form', 'password2', 'The two password fields didn’t match.')


class EditRecordViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.booking = Booking.objects.create(
            user=self.user,
            date=date.today(),
            name="John",
            surname="Doe",
            mobile="1234567890",
            email="john.doe@example.com"
        )

    def test_edit_booking_record(self):
        response = self.client.get(reverse('edit_record', args=['booking', self.booking.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.booking.name)
        self.assertTemplateUsed(response, 'booking/edit_record.html')

        updated_data = {
            'date': date.today(),
            'name': 'Updated',
            'surname': 'User',
            'mobile': '9876543210',
            'email': 'updated@example.com'
        }
        response = self.client.post(reverse('edit_record', args=['booking', self.booking.id]), data=updated_data)
        # Fixed: URL name corrected from 'report_view' to 'report'
        self.assertRedirects(response, reverse('report'))
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.name, 'Updated')
        self.assertEqual(self.booking.surname, 'User')

    def test_invalid_edit_booking_record(self):
        invalid_data = {
            'date': '',
            'name': '',
            'surname': '',
            'mobile': '123',
            'email': 'invalidemail'
        }
        response = self.client.post(reverse('edit_record', args=['booking', self.booking.id]), data=invalid_data)
        # Fixed: error messages updated to match the actual messages in test_drive/forms.py
        self.assertFormError(response, 'form', 'mobile', 'Mobile number must be between 10 and 15 digits.')
        self.assertFormError(response, 'form', 'email', 'Invalid email format.')
