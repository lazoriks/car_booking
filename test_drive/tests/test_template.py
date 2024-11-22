from django.test import TestCase
from django.urls import reverse

class TemplateRenderTest(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_booking_page(self):
        response = self.client.get(reverse('booking_view'))
        self.assertEqual(response.status_code, 302)  
