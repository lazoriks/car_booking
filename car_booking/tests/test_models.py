from django.test import TestCase
from car_booking.models import Product
from decimal import Decimal
from datetime import date


class ProductModelTest(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            engine='V6',
            transmission='Manual',
            year=2020,
            mileage=15000,
            fuel_type='Petrol',
            total_owners=1,
            road_tax=Decimal('150.50'),
            seating_capacity=5,
            color='Red',
            nct_expiry=date(2024, 5, 1)
        )

    def test_product_creation(self):
        product = self.product
        self.assertEqual(product.engine, 'V6')
        self.assertEqual(product.transmission, 'Manual')
        self.assertEqual(product.year, 2020)
        self.assertEqual(product.mileage, 15000)
        self.assertEqual(product.fuel_type, 'Petrol')
        self.assertEqual(product.total_owners, 1)
        self.assertEqual(product.road_tax, Decimal('150.50'))
        self.assertEqual(product.seating_capacity, 5)
        self.assertEqual(product.color, 'Red')
        self.assertEqual(product.nct_expiry, date(2024, 5, 1))

    def test_product_str_method(self):
        product = self.product
        self.assertEqual(str(product), 'Product: V6, 2020')

    def test_product_save(self):
        product = Product.objects.create(
            engine='V8',
            transmission='Automatic',
            year=2021,
            mileage=10000,
            fuel_type='Diesel',
            total_owners=2,
            road_tax=Decimal('200.75'),
            seating_capacity=7,
            color='Blue',
            nct_expiry=date(2025, 8, 1)
        )
        self.assertTrue(Product.objects.filter(engine='V8').exists())
        self.assertEqual(Product.objects.count(), 2)
