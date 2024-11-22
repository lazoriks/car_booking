from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse

class StripePaymentTest(TestCase):
    @patch('stripe.checkout.Session.create')
    def test_create_checkout_session(self, mock_stripe_session):
        mock_stripe_session.return_value = {
            'id': 'test_session_id',
            'url': 'https://checkout.stripe.com/pay/test_session'
        }
        response = self.client.post(reverse('create_checkout_session'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('test_session', response.json()['url'])
