from django.db import models
from django.contrib.auth.models import User


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return f'{self.name} {self.surname} - {self.date}'


class RequestToBuy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    email = models.EmailField(max_length=254)
    mobile = models.CharField(max_length=15)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Request from {self.user.username} on {self.date}'
