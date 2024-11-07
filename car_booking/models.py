from django.db import models


class Product(models.Model):
    engine = models.CharField(max_length=100)
    transmission = models.CharField(max_length=50)
    year = models.IntegerField()
    mileage = models.IntegerField()
    fuel_type = models.CharField(max_length=50)
    total_owners = models.IntegerField()
    road_tax = models.DecimalField(max_digits=10, decimal_places=2)
    seating_capacity = models.IntegerField()
    color = models.CharField(max_length=50)
    nct_expiry = models.DateField()

    def __str__(self):
        return f'Product: {self.engine}, {self.year}'
